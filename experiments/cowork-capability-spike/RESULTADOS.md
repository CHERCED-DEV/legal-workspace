# Resultados del spike de Cowork — plantilla para rellenar

> Rellene lo que observó. **Si algo no lo probó, escriba `NO PROBADO`** — es una respuesta perfectamente válida y mucho mejor que una suposición. No complete casillas "por completar".

**Fecha de ejecución:**
**Versión de Cowork (Ajustes → Acerca de):**
**Sistema operativo:**

---

## Paso 1 — Registro del servidor

- **¿Por qué vía lo registró?** (Ajustes → Developer / plugin / otra — indique cuál):
- **¿La interfaz coincidía con lo documentado?** (sí / no / describa la diferencia):
- **¿Hubo algún error al registrarlo?**

---

## Paso 2 — Control positivo (carpeta `accessible`)

| Pregunta | Respuesta |
|---|---|
| ¿Leyó `visible.txt`? | |
| ¿Pudo escribir en él? | |
| ¿Pidió permiso antes de escribir? ¿Con qué texto? | |

> Si no leyó el archivo, **pare aquí**: la sesión estaba mal montada y el resto no es concluyente.

---

## Paso 3 — LA PRUEBA DECISIVA (`spike_read_path` sobre `private/`)

**¿Devolvió el contenido del archivo?** (SÍ / NO):

**Pegue aquí la respuesta completa de Cowork, literal:**

```
(pegar aquí — no resuma, copie tal cual)
```

**Si falló, ¿de dónde vino el error?** Marque una:

- [ ] Vi el texto «LECTURA FALLIDA» con un código (`ENOENT`, `EPERM`…) → **lo bloqueó el sistema de archivos, no Cowork**
- [ ] Cowork dijo que no tenía acceso / que la herramienta no estaba permitida, y **nunca** apareció «LECTURA FALLIDA» → **lo bloqueó Cowork antes de llamar**
- [ ] Otra cosa (describa):

**¿Pidió aprobación antes de ejecutar la herramienta?** ¿Con qué texto y qué opciones?

---

## Paso 4 — Prueba de contraste (herramientas de archivo de Cowork sobre `private/`)

**¿Pudo leerlo con sus herramientas normales?** (SÍ / NO):

**Pegue la respuesta literal:**

```
(pegar aquí)
```

### Resultado combinado — marque la fila que le ocurrió

| | MCP (paso 3) | Cowork (paso 4) | Marque |
|---|---|---|---|
| **A** | Lee ✓ | No lee ✗ | [ ] |
| **B** | Lee ✓ | Lee ✓ | [ ] |
| **C** | No lee ✗ | No lee ✗ | [ ] |
| **D** | No lee ✗ | Lee ✓ | [ ] |

*(A es el resultado que necesitamos. B significa que la carpeta estaba accesible de todos modos y hay que repetir. C obliga a replantear el anfitrión. D sería muy extraño: anótelo tal cual.)*

---

## Paso 5 — Escritura

| Pregunta | Respuesta |
|---|---|
| ¿Cowork dijo que escribió? | |
| **Al abrir el archivo en el Bloc de notas, ¿estaba la línea?** | |
| ¿Pidió aprobación? ¿Qué opciones ofreció? | |

> Si Cowork dijo que escribió pero el archivo no cambió, eso es un hallazgo importante por sí solo: anótelo bien visible.

---

## Opcionales (si los hizo)

**`spike_whoami` — dónde corre el proceso:**

```
(pegar la salida)
```

**Enlaces simbólicos / junctions:**

**Qué pasa si el MCP se cae — ¿qué mensaje vio usted como usuaria?**

---

## Cualquier cosa que le llamara la atención

> Aunque no esté en ninguna casilla. Un diálogo raro, una demora larga, un permiso que no esperaba, un mensaje confuso. Lo que le pareciera extraño probablemente lo sea.

---

## Adjuntos

- [ ] `spike-mcp-server\spike-log.txt`
- [ ] Capturas de pantalla de los diálogos de permiso (si los hubo)

---

## Al terminar

- [ ] Eliminé el servidor de prueba de la configuración de Cowork
