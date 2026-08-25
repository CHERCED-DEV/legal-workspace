# Servidor MCP del spike — NON-PRODUCTION

Instrumento de medida para el Cowork Capability Spike. **No es código de producción.**

- Sin dependencias. Requiere solo Node.js.
- Expone tres tools: `spike_read_path`, `spike_write_path`, `spike_whoami`.
- Lee y escribe **cualquier ruta** que se le pida, a propósito: eso es justamente lo que se quiere medir.
- Registra todo en `spike-log.txt` (se genera al ejecutarse).

**Prohibido importarlo desde `src/`.** Elimínelo de la configuración de Cowork al terminar la prueba.

Instrucciones de uso: `../INSTRUCCIONES.md`
