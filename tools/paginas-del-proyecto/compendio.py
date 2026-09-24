"""Empaqueta un proyecto para enviarlo a quien declara, sin lo que no debe viajar:
los WAV intermedios (.trabajo), el .zip de la entrega (duplica su carpeta),
_fuentes (no enviar), las carpetas _anteriores y el mapa del dueño. No borra ni
mueve nada del proyecto.

Mide ademas el riesgo de MAX_PATH (260 caracteres en Windows): la ruta interna mas
larga, y la peor ruta que escribira la pagina al guardar, suponiendo que se extrae
en Descargas con un nombre de usuario largo. Medido en un caso real: con 267
caracteres Edge no abre la pagina («No se encuentra el archivo»).

Uso:  python compendio.py <proyecto> <salida.zip>
      (nombre corto para el .zip: el Explorador crea una carpeta con ese nombre)
"""
import os
import sys
import zipfile

LIMITE = 260
BASE_PEOR = r"C:\Users\Nombre.Largo.De.Usuario\Downloads"
# Lo mas largo que escribe la pagina de cada grabacion al guardar (guardado.js):
# «<titulo> - AAAA-MM-DD HH.MM.SS - en curso anterior.json» en 2-Borradores/Lo que declaré/<entrega>/
GUARDADO_PEOR = "2-Borradores/Lo que declaré/{entrega}/Transcripción del Audio 10 - 2026-12-31 23.59.59 - en curso anterior.json"


def main():
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    proy, salida = os.path.abspath(sys.argv[1]), os.path.abspath(sys.argv[2])
    if os.path.exists(salida):
        raise SystemExit("DETENIDO: ya existe " + salida)
    raiz = os.path.basename(proy)
    fuera, dentro, peso, entregas = set(), 0, 0, []
    with zipfile.ZipFile(salida, "w") as z:
        for r, ds, fs in os.walk(proy):
            rel = os.path.relpath(r, proy)
            partes = [] if rel == "." else rel.split(os.sep)
            if any(p in (".trabajo", "_fuentes (no enviar)", "_anteriores") for p in partes):
                fuera.add(rel)
                ds[:] = []
                continue
            if len(partes) == 2 and partes[0] == "2-Borradores" and partes[1] == "Entregas":
                entregas += [d for d in ds if d.startswith("ENTREGA - ")]
            for f in sorted(fs):
                p = os.path.join(r, f)
                if f.endswith(".zip") or f.startswith("Mapa del entregable"):
                    fuera.add(os.path.join(rel, f))
                    continue
                z.write(p, os.path.join(raiz, os.path.relpath(p, proy)),
                        zipfile.ZIP_STORED if f.lower().endswith((".mp4", ".m4a", ".jpeg", ".jpg", ".png", ".docx", ".pdf")) else zipfile.ZIP_DEFLATED)
                dentro += 1
                peso += os.path.getsize(p)
    with zipfile.ZipFile(salida) as z:
        if z.testzip() is not None:
            raise SystemExit("DETENIDO: el zip salio corrupto")
        nombres = z.namelist()
    envoltura = os.path.splitext(os.path.basename(salida))[0]
    base = os.path.join(BASE_PEOR, envoltura)
    larga = max(nombres, key=len)
    print("archivos: %d · %.0f MB · zip %.0f MB" % (dentro, peso / 1e6, os.path.getsize(salida) / 1e6))
    print("fuera:", sorted(fuera))
    print("ruta interna mas larga: %d caracteres" % len(larga))
    print("extraida en Descargas (usuario largo): %d de %d" % (len(base) + 1 + len(larga), LIMITE))
    for e in entregas or ["ENTREGA - X"]:
        g = os.path.join(raiz, GUARDADO_PEOR.format(entrega=e))
        n = len(base) + 1 + len(g)
        print("peor ruta al guardar (%s): %d de %d%s" % (e, n, LIMITE, "  <-- RIESGO" if n > LIMITE - 20 else ""))


if __name__ == "__main__":
    main()
