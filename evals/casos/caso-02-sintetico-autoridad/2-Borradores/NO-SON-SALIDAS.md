# Estos archivos son fixtures, no salidas de los métodos

**Y por eso las guardas de `evals/scripts/comprobar-salidas.sh` los saltan.**

Los cuatro `.md` de esta carpeta están escritos **en forma comprimida a propósito**: son el material que `caso-02` necesita para probar otras cosas —el reconocimiento de la marca ` - REVISADO` en sus cinco formas, la cadena que se detiene sin ella, el conteo de la entrega por lado—, no ejemplos de cómo se ve una salida completa.

**Qué les falta, y es deliberado:** los encabezados `## H-01`, la línea `Estado:` de cada ficha, el bloque `CONTEO`. Un método real los produce; estos no, porque no los produjo un método.

> **Por qué esto se escribe en vez de arreglarse.** La primera vez que las guardas corrieron sobre toda la carpeta, marcaron los cuatro como *«la salida no declara su conteo, y el método lo pide»*. **Es un aviso correcto sobre un archivo que no es una salida.** Se podía silenciar de dos maneras: rellenándolos —lo que rompería las pruebas que dependen de su forma exacta— o dejando el aviso encendido para siempre, que es la manera de que nadie lo vuelva a mirar. **Se elige la tercera: decir qué son.**

**Las salidas de verdad, medidas contra su truth set, están en `caso-03`.**
