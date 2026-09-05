# -*- coding: utf-8 -*-
"""Busca dentro de la carpeta de un caso sin gastar lectura del modelo.

Recorre el texto de referencia, los .md y .txt de 2-Borradores, y -si estan
disponibles- los .docx y .pdf, y devuelve donde aparece lo que se busca.

    python buscar.py "<carpeta del caso>" "cadena" [--exacto] [--contexto 90]
                     [--solo recibidos|borradores] [--json]

Lo que este programa NO hace, y va escrito aqui porque es la parte que
importa:

  * NO decide si algo esta o no esta en el expediente. Lo que busca es el
    TEXTO EXTRAIDO, y el reconocedor falla callandose: una pagina puede
    contener la palabra y no haberla devuelto nunca. Cero resultados
    significa "no aparece en lo extraido", jamas "no esta en el papel".
  * NO cita. Devuelve donde mirar; la cita sale de abrir el documento.
  * NO escribe nada en la carpeta del caso.
"""
import argparse
import io
import json
import re
import sys
import unicodedata
import zipfile
from pathlib import Path

EXT_TEXTO = {'.md', '.txt'}
EXT_IMAGEN = {'.jpg', '.jpeg', '.png', '.tif', '.tiff', '.bmp', '.heic'}
NO_CITABLE = ("Esto es el texto EXTRAIDO, no el documento. El reconocedor omite "
              "en silencio: cero resultados NO significa que no este en el papel.")
# Una aparicion dentro de 2-Borradores o 3-Para presentar NO es material del
# caso: es trabajo del sistema, o de ella. El §2 de seis SKILL.md dice que el
# trabajo del sistema es pista y nunca origen, y una busqueda que devuelve las
# tres cosas en una sola lista invita justo a citar la que no se puede citar.
NO_ES_MATERIAL = ("De estos renglones, %d estan FUERA de 1-Documentos recibidos: "
                  "no son material del caso.\n"
                  "  Lo que hay en 2-Borradores es trabajo del sistema o borradores "
                  "de ella; lo de 3-Para presentar es lo que ella dio por terminado.\n"
                  "  Sirven para saber donde mirar. La cita sale del documento "
                  "original, siempre.")


def origen(rel):
    """Material recibido, o no. Es la unica distincion que cambia que se puede citar."""
    return 'material' if str(rel).replace('\\', '/').startswith('1-Documentos recibidos') else 'otro'
# Un expediente colombiano no contiene ideogramas: si salen, es basura del OCR.
CJK = re.compile(r'[一-鿿぀-ヿ가-힯]')


def plano(s):
    """Sin tildes y en minusculas, para que 'Galvez' encuentre 'Gálvez'."""
    d = unicodedata.normalize('NFD', s)
    return ''.join(c for c in d if unicodedata.category(c) != 'Mn').lower()


def texto_docx(ruta):
    try:
        with zipfile.ZipFile(ruta) as z:
            xml = z.read('word/document.xml').decode('utf-8', 'replace')
        xml = re.sub(r'</w:p>', '\n', xml)
        return re.sub(r'<[^>]+>', '', xml)
    except Exception:
        return None


def texto_pdf(ruta):
    """Solo si hay con que. Un PDF de imagenes no tiene capa de texto."""
    try:
        from pypdf import PdfReader
    except ImportError:
        try:
            from PyPDF2 import PdfReader
        except ImportError:
            return None
    try:
        return '\n'.join((p.extract_text() or '') for p in PdfReader(str(ruta)).pages)
    except Exception:
        return None


def leer(ruta):
    e = ruta.suffix.lower()
    if e in EXT_TEXTO:
        try:
            return io.open(ruta, encoding='utf-8', errors='replace').read()
        except Exception:
            return None
    if e == '.docx':
        return texto_docx(ruta)
    if e == '.pdf':
        return texto_pdf(ruta)
    return None


def _carpetas(caso, ambito):
    c = []
    if ambito in (None, 'recibidos'):
        c.append(caso / '1-Documentos recibidos')
    if ambito in (None, 'borradores'):
        c += [caso / '2-Borradores', caso / '3-Para presentar']
    return [x for x in c if x.is_dir()]


def piezas(caso, ambito):
    for c in _carpetas(caso, ambito):
        for f in sorted(c.rglob('*')):
            if f.is_file() and f.suffix.lower() in EXT_TEXTO | {'.docx', '.pdf'}:
                yield f


def imagenes(caso, ambito):
    """Lo que esta busqueda NO puede mirar. Callarlo seria el defecto."""
    out = []
    for c in _carpetas(caso, ambito):
        out += [f for f in sorted(c.rglob('*'))
                if f.is_file() and f.suffix.lower() in EXT_IMAGEN]
    return out


def buscar(caso, aguja, exacto=False, contexto=90, ambito=None):
    patron = (re.compile(re.escape(aguja), re.I) if exacto
              else re.compile(re.escape(plano(aguja))))
    hallazgos, leidos, ilegibles = [], [], []

    for f in piezas(caso, ambito):
        t = leer(f)
        if t is None:
            ilegibles.append(str(f.relative_to(caso)))
            continue
        leidos.append(str(f.relative_to(caso)))
        lineas = t.split('\n')
        for n, linea in enumerate(lineas, 1):
            campo = linea if exacto else plano(linea)
            # Un renglon se devuelve UNA vez, aunque la cadena aparezca varias.
            # Repetirlo idéntico no dice donde mirar mejor y ademas hincha el
            # conteo, que es lo que ella lee. Las veces se dicen aparte.
            veces = len(patron.findall(campo))
            if not veces:
                continue
            m = patron.search(campo)
            ini = max(0, m.start() - contexto)
            fin = min(len(linea), m.end() + contexto)
            hallazgos.append({
                'archivo': str(f.relative_to(caso)),
                'linea': n,
                'veces': veces,
                'texto': linea[ini:fin].strip(),
                'sospechoso': bool(CJK.search(linea)) or len(linea.strip()) < 3,
            })
    return hallazgos, leidos, ilegibles


def main():
    ap = argparse.ArgumentParser(description='Busca dentro de la carpeta de un caso.')
    ap.add_argument('caso')
    ap.add_argument('cadena')
    ap.add_argument('--exacto', action='store_true',
                    help='distingue tildes y respeta el texto tal cual')
    ap.add_argument('--contexto', type=int, default=90)
    ap.add_argument('--solo', choices=['recibidos', 'borradores'])
    ap.add_argument('--json', action='store_true')
    a = ap.parse_args()

    caso = Path(a.caso).expanduser()
    if not caso.is_dir():
        sys.stderr.write('No existe la carpeta: %s\n' % caso)
        raise SystemExit(2)

    hall, leidos, ilegibles = buscar(caso, a.cadena, a.exacto, a.contexto, a.solo)
    imgs = imagenes(caso, a.solo)

    if a.json:
        for x in hall:
            x['origen'] = origen(x['archivo'])
        print(json.dumps({'cadena': a.cadena, 'hallazgos': hall, 'leidos': leidos,
                          'ilegibles': ilegibles,
                          'fuera_de_recibidos': len([x for x in hall if x['origen'] != 'material']),
                          'imagenes_no_miradas': [str(x.relative_to(caso)) for x in imgs],
                          'aviso': NO_CITABLE},
                         ensure_ascii=False, indent=1))
        return

    print('Buscando «%s» en %s' % (a.cadena, caso.name))
    print('Se miraron %d archivos con texto legible.' % len(leidos))
    if ilegibles:
        print('NO SE PUDIERON LEER %d (formato no soportado o archivo dañado): %s'
              % (len(ilegibles), ', '.join(ilegibles[:6])
                 + (' ...' if len(ilegibles) > 6 else '')))
    if imgs:
        print('NO SE MIRARON %d IMAGENES: una fotografia no tiene texto que buscar.'
              % len(imgs))
        print('  Lo que se busco de ellas es lo que el OCR llego a extraer, si se '
              'extrajo. Para mirarlas hay que abrirlas.')
    print()

    if not hall:
        print('CERO APARICIONES en lo que se pudo leer.')
        print(NO_CITABLE)
        return

    actual = None
    dudosos = 0
    for x in hall:
        if x['archivo'] != actual:
            actual = x['archivo']
            etiqueta = '' if origen(actual) == 'material' else '   <- NO es material del caso'
            print('### %s%s' % (actual, etiqueta))
        marca = '  [renglon dudoso: basura probable del OCR]' if x['sospechoso'] else ''
        if x['sospechoso']:
            dudosos += 1
        veces = '  [%d veces en este renglon]' % x['veces'] if x.get('veces', 1) > 1 else ''
        print('  linea %-5d %s%s%s' % (x['linea'], x['texto'], veces, marca))
    print()
    fuera = len([x for x in hall if origen(x['archivo']) != 'material'])
    total = sum(x.get('veces', 1) for x in hall)
    extra = ' (%d apariciones: alguna se repite en su renglon)' % total if total != len(hall) else ''
    print('%d renglones en %d archivos%s.%s'
          % (len(hall), len({x['archivo'] for x in hall}), extra,
             ('  %d en renglones dudosos.' % dudosos) if dudosos else ''))
    if fuera:
        print(NO_ES_MATERIAL % fuera)
    print(NO_CITABLE)


if __name__ == '__main__':
    main()
