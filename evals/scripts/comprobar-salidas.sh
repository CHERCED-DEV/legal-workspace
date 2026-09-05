#!/bin/sh
# Pasa las tres guardas sobre TODAS las salidas de los casos de banco.
#
# Existe porque hasta hoy se corrian a mano, una por una, y eso es exactamente
# el trabajo que este repositorio ya demostro que no se le puede confiar a la
# atencion: cinco cuentas mal hechas el mismo dia, ninguna encontrada releyendo.
#
#   sh evals/scripts/comprobar-salidas.sh
#
# Devuelve distinto de cero si alguna salida tiene algo que mirar.
cd "$(dirname "$0")/../.."
fallos=0

for caso in evals/casos/*/; do
  material="$caso/1-Documentos recibidos"
  borradores="$caso/2-Borradores"
  [ -d "$borradores" ] || continue
  printf '\n=== %s\n' "$(basename "$caso")"

  # Una carpeta puede declarar que lo suyo son fixtures y no salidas. Se
  # respeta y se dice: un aviso correcto sobre un archivo que no es una salida
  # es, si se deja encendido, la manera de que nadie vuelva a mirar ninguno.
  if [ -f "$borradores/NO-SON-SALIDAS.md" ]; then
    printf '    saltada: la carpeta declara que sus .md son fixtures\n'
    printf '    (ver %s/NO-SON-SALIDAS.md)\n' "$borradores"
    continue
  fi

  for f in "$borradores"/*.md; do
    [ -e "$f" ] || continue
    nombre=$(basename "$f")
    printf '\n--- %s\n' "$nombre"

    # 1. El conteo que la salida declara contra las fichas que tiene.
    python3 plugins/despacho/scripts/contar_fichas.py "$f" 2>/dev/null | tail -3
    python3 plugins/despacho/scripts/contar_fichas.py "$f" >/dev/null 2>&1 \
      || fallos=$((fallos+1))

    # 2. Numeros y fechas que solo pueden salir de una cuenta.
    if [ -d "$material" ]; then
      python3 evals/scripts/buscar_cuentas.py "$f" --material "$material" \
        2>/dev/null | tail -1
      python3 evals/scripts/buscar_cuentas.py "$f" --material "$material" \
        >/dev/null 2>&1 || fallos=$((fallos+1))
    fi

    # 3. Las afirmaciones prohibidas, solo donde hay truth set.
    case "$caso" in
      *caso-03*)
        python3 evals/scripts/puntuar_caso03.py "$f" 2>/dev/null | tail -2 | head -1
        python3 evals/scripts/puntuar_caso03.py "$f" >/dev/null 2>&1 \
          || fallos=$((fallos+1))
        ;;
    esac
  done
done

printf '\n%s comprobacion(es) con algo que mirar\n' "$fallos"
exit $fallos
