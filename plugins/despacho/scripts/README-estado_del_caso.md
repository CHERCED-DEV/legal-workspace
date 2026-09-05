# estado_del_caso.py — reemplazar la cabecera sin tocar lo que ella escribió

**Qué es.** El programa que ejecuta `/estado-del-caso` en su Fase 6 para escribir `0-Estado del caso (no editar).txt`. **Reemplaza solo la cabecera.** De la línea `NOTAS SUYAS` hacia abajo, el archivo se conserva **byte a byte**.

**Por qué existe, y por qué es un programa y no una instrucción más.** En este sistema no hay copiar y pegar: cada vez que un texto aparece en una salida del modelo, se **re-emite palabra por palabra**. El archivo de estado es el único punto del producto donde vuelve a salir por esa vía **un texto escrito por ella**, y una normalización silenciosa —una tilde, unas comillas, dos renglones que se juntan— **no se nota**. Aquí la cola se copia como bytes y se comprueba después de escribir: si cambió uno solo, se restaura la copia y no hay cambio. Ver `docs/specs/SPEC-06-escritura-dirigida-del-estado.md` y `PM-M-8`.

## Uso

```bash
python estado_del_caso.py "<carpeta del caso>" --comprobar
python estado_del_caso.py "<carpeta del caso>" --cabecera "<archivo con la cabecera nueva>"
python estado_del_caso.py "<carpeta del caso>" --cabecera "<...>" --crear
```

`--comprobar` es lo que se corre en la Fase 0: dice si el archivo existe, si tiene la línea marcadora y **cuántos renglones suyos hay debajo** — nunca su contenido.

## Lo que hace por su cuenta, y son las tres cosas que no se pueden dejar a la buena voluntad

1. **Guarda la copia previa** en `2-Borradores/0-Estado del caso — anterior (AAAA-MM-DD).txt`, con ` (2)` si ya hay una de hoy y **sin sobrescribir nunca**. Si no puede copiar, **no escribe**.
2. **Conserva de la marca hacia abajo byte a byte.** Funciona igual con archivos guardados por Windows en `cp1252`.
3. **Comprueba después de escribir** que la cola quedó idéntica. Si no, restaura la copia y devuelve error.

## Códigos de salida

| Código | Qué pasó |
|---|---|
| 0 | Escrito, o comprobado |
| 1 | Error de uso |
| 2 | El archivo no existe y no se pasó `--crear` |
| 3 | **No hay línea `NOTAS SUYAS`: no se escribió nada.** Sin ella no hay forma de saber dónde empieza lo suyo |
| 4 | No se pudo guardar la copia previa. No se escribió nada |
| 5 · 6 | Falló la escritura o la comprobación. **Se restauró la copia** |

## Lo que NO hace

- **No imprime las notas de ella.** Lo que no se imprime no se puede parafrasear.
- **No entiende el formato de la cabecera**: la recibe escrita y la pega. Un programa que entendiera la plantilla sería un segundo sitio donde vive, y dos sitios derivan (ADR-014, invariante 6).
- **No renombra, no mueve y no borra** nada.

## Las pruebas

`evals/scripts/test_estado_del_caso.py` — trece, y **capaces de fallar**: se comprobaron con dos mutantes, uno que normaliza una comilla al escribir la cola (cae con 3 fallos) y otro que reescribe entero cuando no hay marca (cae con 2). El control positivo es `test_la_cabecera_si_cambia`: sin él, un programa que no escribiera nada pasaría el resto con nota perfecta.

```bash
python3 evals/scripts/test_estado_del_caso.py
```
