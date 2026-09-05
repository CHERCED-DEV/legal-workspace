#!/bin/sh
# Todas las pruebas de esta carpeta, de una vez.
#   sh evals/scripts/correr-todo.sh
# Devuelve distinto de cero si alguna falla, para poder colgarlo de un hook.
set -e
cd "$(dirname "$0")/../.."
fallos=0
for f in evals/scripts/test_*.py; do
  printf '\n=== %s\n' "$f"
  python3 "$f" 2>&1 | tail -4 || fallos=$((fallos+1))
  python3 "$f" >/dev/null 2>&1 || fallos=$((fallos+1))
done
printf '\n=== evals/knowledge-pack\n'
python3 evals/knowledge-pack/test_vias.py 2>&1 | tail -3
python3 evals/knowledge-pack/test_vias.py >/dev/null 2>&1 || fallos=$((fallos+1))
printf '\n=== las guardas sobre las salidas de los casos\n'
sh evals/scripts/comprobar-salidas.sh 2>&1 | tail -2
sh evals/scripts/comprobar-salidas.sh >/dev/null 2>&1 || fallos=$((fallos+1))

printf '\n%s archivos de prueba con fallos\n' "$fallos"
exit $fallos
