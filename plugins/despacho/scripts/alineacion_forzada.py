# -*- coding: utf-8 -*-
"""alineacion_forzada — poner cada palabra donde de verdad suena.

Modulo de apoyo de alinear_tiempos.py. No se ejecuta solo.

EL PROBLEMA. Las marcas de tiempo que trae la transcripcion no vienen de oir el
audio buscando cada palabra: salen de la atencion del propio reconocedor,
estiradas con DTW. Es una estimacion indirecta, y se nota sobre todo en las
fronteras entre dos personas, que es donde una frase puede acabar en boca ajena.

QUE HACE ESTO. Alineacion forzada: el texto YA se sabe, asi que en vez de
adivinar que se dijo, se busca el reparto de ese texto exacto entre los
fotogramas del audio que mejor lo explica. Un modelo acustico CTC da, por cada
20 ms, cuanto se parece ese instante a cada letra; y un Viterbi encuentra el
unico camino que recorre las letras en orden sin saltarse ninguna.

LA GUARDA. Un alineador siempre devuelve un resultado, tambien cuando el audio
no dice lo que el texto afirma: reparte las letras por donde puede y calla. Por
eso cada ventana se descodifica ANTES a ciegas y se compara con el texto
conocido; si no se parecen, esa ventana se deja intacta y se dice. Sin esa
comprobacion esto seria un instrumento que miente.

Modelo: wav2vec2-large-xlsr-53-spanish (Apache-2.0). Los otros candidatos
-- MMS, VoxPopuli -- son CC BY-NC y no sirven para un despacho.
"""
import re, unicodedata
import numpy as np

MODELO = "jonatasgrosman/wav2vec2-large-xlsr-53-spanish"
NEG = -1e30


def normalizar(t):
    t = unicodedata.normalize("NFC", (t or "").lower())
    t = t.replace("ü", "u")
    return re.sub(r"\s+", " ", t).strip()


def palabras_de(texto, vocab):
    """Cada palabra con las letras que el modelo sabe reconocer. Las que no
    dejan ninguna (numeros, simbolos) se devuelven vacias: conservan su sitio en
    la lista pero no se alinean."""
    fuera = []
    for p in normalizar(texto).split(" "):
        ids = [vocab[c] for c in p if c in vocab]
        fuera.append((p, ids))
    return fuera


def viterbi(logp, fichas, blanco):
    """El camino de maxima verosimilitud que recorre `fichas` en orden.

    Entre ficha y ficha puede haber blanco -- por eso la secuencia se extiende
    intercalandolo --, y se permite saltarse ese blanco salvo entre dos letras
    iguales, donde hace falta para no fundirlas en una."""
    F, S = logp.shape[0], 2 * len(fichas) + 1
    ext = np.full(S, blanco, dtype=np.int64)
    ext[1::2] = fichas
    salto = np.zeros(S, dtype=bool)
    salto[2:] = (ext[2:] != blanco) & (ext[2:] != ext[:-2])

    a = np.full(S, NEG)
    a[0] = logp[0, ext[0]]
    if S > 1:
        a[1] = logp[0, ext[1]]
    atras = np.zeros((F, S), dtype=np.int8)
    idx = np.arange(S)
    for f in range(1, F):
        previo = np.concatenate(([NEG], a[:-1]))
        salta = np.where(salto, np.concatenate(([NEG, NEG], a[:-2])), NEG)
        cand = np.stack([a, previo, salta])
        arg = np.argmax(cand, axis=0)
        a = cand[arg, idx] + logp[f, ext]
        atras[f] = arg

    s = S - 1 if a[S - 1] >= a[S - 2] else S - 2
    camino = np.zeros(F, dtype=np.int64)
    for f in range(F - 1, -1, -1):
        camino[f] = s
        s -= int(atras[f, s])
    return camino


def tramos_por_ficha(camino, n):
    """Primer y ultimo fotograma de cada ficha."""
    fuera = []
    for k in range(n):
        d = np.where(camino == 2 * k + 1)[0]
        fuera.append((int(d[0]), int(d[-1])) if len(d) else None)
    return fuera


def distancia(a, b):
    """Levenshtein, para comparar lo que se oye con lo que dice el texto."""
    if not a or not b:
        return max(len(a), len(b))
    ant = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        act = [i]
        for j, cb in enumerate(b, 1):
            act.append(min(ant[j] + 1, act[j - 1] + 1, ant[j - 1] + (ca != cb)))
        ant = act
    return ant[-1]


class Alineador(object):
    def __init__(self, modelo=MODELO, hilos=None):
        import torch
        from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor
        self.torch = torch
        if hilos:
            torch.set_num_threads(hilos)
        self.proc = Wav2Vec2Processor.from_pretrained(modelo)
        self.mod = Wav2Vec2ForCTC.from_pretrained(modelo).eval()
        self.vocab = {c: i for c, i in self.proc.tokenizer.get_vocab().items() if len(c) == 1}
        self.blanco = self.proc.tokenizer.get_vocab()[self.proc.tokenizer.pad_token]
        self.sep = self.proc.tokenizer.get_vocab()[self.proc.tokenizer.word_delimiter_token]
        self.inv = {i: c for c, i in self.proc.tokenizer.get_vocab().items()}

    def probabilidades(self, onda):
        t = self.torch
        with t.inference_mode():
            x = self.proc(onda, sampling_rate=16000, return_tensors="pt").input_values
            y = self.mod(x).logits[0]
            return t.log_softmax(y, dim=-1).numpy().astype(np.float64)

    def a_ciegas(self, logp):
        """Lo que el modelo oye sin mirar el texto: la guarda contra alinear
        sobre audio que no corresponde."""
        ids, fuera, ant = logp.argmax(axis=1), [], -1
        for i in ids:
            if i != ant and i != self.blanco:
                fuera.append(self.inv.get(int(i), ""))
            ant = i
        return "".join(fuera).replace("|", " ").strip()

    def alinear(self, onda, palabras, cer_max=0.45):
        """(tiempos por palabra, error de la descodificacion a ciegas).

        Devuelve None en los tiempos si la ventana no supera la guarda."""
        con = [(p, ids) for p, ids in palabras if ids]
        if not con:
            return None, None
        logp = self.probabilidades(onda)
        oido = self.a_ciegas(logp)
        dicho = " ".join(p for p, _ in con)
        cer = distancia(oido, dicho) / max(len(dicho), 1)
        if cer > cer_max:
            return None, cer

        fichas, tramo_de = [], []
        for _, ids in con:
            if fichas:
                fichas.append(self.sep)
            a = len(fichas)
            fichas.extend(ids)
            tramo_de.append((a, len(fichas) - 1))
        if len(fichas) >= logp.shape[0]:
            return None, cer

        camino = viterbi(logp, fichas, self.blanco)
        tr = tramos_por_ficha(camino, len(fichas))
        seg = len(onda) / 16000.0 / logp.shape[0]
        fuera, k = [], 0
        for p, ids in palabras:
            if not ids:
                fuera.append(None)
                continue
            a, b = tramo_de[k]
            k += 1
            if tr[a] is None or tr[b] is None:
                fuera.append(None)
            else:
                fuera.append((tr[a][0] * seg, (tr[b][1] + 1) * seg))
        return fuera, cer
