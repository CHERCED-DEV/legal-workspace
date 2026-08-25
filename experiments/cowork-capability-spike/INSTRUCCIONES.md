# Cómo ejecutar el spike de Cowork — instrucciones paso a paso

**Qué vamos a averiguar:** si un servidor MCP local puede leer una carpeta que **no** está adjuntada a la sesión de Cowork, mientras las herramientas de archivo del propio Cowork **no** pueden.

De esa asimetría depende que el expediente pueda protegerse tal como está diseñado. **Es el único bloqueante que queda.**

Tiempo estimado: **20–30 minutos** para la prueba decisiva.

---

## Antes de empezar

**Necesita:** Cowork Desktop instalado y Node.js. (Verificado en este equipo: **Node v20.19.0** ✓)

**No necesita** instalar nada más: el servidor de prueba no tiene dependencias.

**Una advertencia:** el servidor de prueba lee y escribe cualquier ruta que se le pida, a propósito — es un instrumento de medida, no un componente del producto. Bórrelo cuando termine (§6).

---

## Paso 1 — Registrar el servidor de prueba en Cowork

La ruta del servidor es:

```
C:\Users\HITMA\Desktop\legal-workspace\experiments\cowork-capability-spike\spike-mcp-server\server.js
```

En Cowork, busque dónde se añaden servidores MCP locales. Según la documentación oficial está en **Ajustes → Developer**, pero **la ubicación exacta no está verificada**: si no la encuentra ahí, mire en Ajustes → Conectores, o en la gestión de plugins.

Los datos a introducir:

| Campo | Valor |
|---|---|
| Nombre | `spike` |
| Comando | `node` |
| Argumentos | la ruta completa de `server.js` de arriba |

Si Cowork le pide un JSON en vez de campos, use esto:

```json
{
  "mcpServers": {
    "spike": {
      "command": "node",
      "args": ["C:\\Users\\HITMA\\Desktop\\legal-workspace\\experiments\\cowork-capability-spike\\spike-mcp-server\\server.js"]
    }
  }
}
```

**Anote:** por cuál de las dos vías lo registró, y si la interfaz coincide con lo que dice la documentación o no. Eso ya es un dato del informe.

---

## Paso 2 — Comprobar que la sesión está bien montada (control positivo)

Abra una **sesión nueva** en Cowork y adjunte **únicamente** esta carpeta:

```
C:\Users\HITMA\Desktop\legal-workspace\experiments\cowork-capability-spike\experimental-root\accessible
```

**No adjunte `experimental-root` entera. No adjunte `private`.** Solo `accessible`.

Pídale a Cowork, con estas palabras:

> Lee el archivo visible.txt de la carpeta que te adjunté y muéstrame su contenido.

**Debe leerlo.** Si no puede, la sesión está mal montada y **no continúe**: el resto de la prueba no significaría nada.

Pídale ahora:

> Añade una línea al final de visible.txt que diga: prueba de escritura.

**Anote** si lo consigue y si le pidió permiso antes.

---

## Paso 3 — LA PRUEBA DECISIVA

En **la misma sesión**, sin adjuntar nada más, pídale exactamente esto:

> Usa la herramienta spike_read_path con esta ruta: `C:\Users\HITMA\Desktop\legal-workspace\experiments\cowork-capability-spike\experimental-root\private\private.txt`

**Los dos resultados posibles, y qué significan:**

| Lo que ocurre | Qué significa |
|---|---|
| **Devuelve el contenido** del archivo (empieza por «CONTROL NEGATIVO…») | El MCP local **no** está confinado a las carpetas adjuntadas. **El diseño del perímetro funciona.** Es el resultado que esperamos. |
| **Falla** | Copie el mensaje de error **literal y completo**. Es igual de valioso: significa que hay que cambiar de anfitrión o hacer del Core un proceso independiente. |

**Si falla, hay un detalle que lo decide todo:** si el mensaje que ve empieza por «LECTURA FALLIDA» y menciona un código como `ENOENT` o `EPERM`, el error viene **del servidor**. Si en cambio Cowork dice algo como «no tengo acceso» o «esa herramienta no está permitida» y nunca aparece el texto «LECTURA FALLIDA», entonces **fue Cowork quien lo bloqueó antes de llamar**. Son dos conclusiones opuestas. Anote cuál de las dos vio.

---

## Paso 4 — La prueba de contraste (imprescindible)

**Sin este paso, el paso 3 no demuestra nada.** Hay que descartar que la carpeta estuviera accesible de todos modos.

En **la misma sesión**, pídale:

> Ahora, sin usar ninguna herramienta del servidor spike, lee con tus herramientas de archivo normales este archivo: `C:\Users\HITMA\Desktop\legal-workspace\experiments\cowork-capability-spike\experimental-root\private\private.txt`

**Lo que buscamos es la asimetría:**

| MCP (paso 3) | Herramientas de Cowork (paso 4) | Conclusión |
|---|---|---|
| Lee ✓ | **No** lee ✗ | **El resultado que necesitamos.** El diseño funciona. |
| Lee ✓ | Lee ✓ | La carpeta estaba accesible igualmente: la prueba no demuestra nada. Revise que no adjuntó `private` ni la carpeta padre. |
| No lee ✗ | No lee ✗ | El MCP está confinado igual que el host. **Hay que replantear el anfitrión.** |

---

## Paso 5 — Prueba de escritura (2 minutos)

> Usa la herramienta spike_write_path sobre la ruta `C:\Users\HITMA\Desktop\legal-workspace\experiments\cowork-capability-spike\experimental-root\private\private.txt` con el texto: escritura desde MCP.

Después **abra ese archivo con el Bloc de notas** (fuera de Cowork) y compruebe si la línea se añadió de verdad. No se fíe de lo que diga Cowork: compruébelo en disco.

**Anote también** si Cowork le pidió aprobación antes de ejecutar la herramienta, con qué texto exacto, y qué opciones le ofreció (*Permitir una vez*, *Permitir para esta tarea*, *Permitir siempre*, *Denegar*).

---

## Paso 6 — Al terminar

1. Rellene la plantilla `RESULTADOS.md` (está en esta misma carpeta) y me la pasa.
2. Adjunte también el archivo `spike-mcp-server\spike-log.txt`, que se genera solo y registra todo lo que el servidor hizo.
3. **Elimine el servidor de prueba de la configuración de Cowork.** No debe quedar registrado: lee y escribe cualquier ruta a propósito.

---

## Si quiere ir más allá (opcional, no bloqueante)

Estas pruebas aportan, pero **no** hacen falta para desbloquear el diseño:

- **Dónde corre el proceso.** Pídale: «usa la herramienta spike_whoami». Le dirá el directorio, el usuario y la plataforma del proceso. Confirma si el MCP corre en su equipo o en una máquina virtual.
- **Enlaces simbólicos.** Cree un acceso directo dentro de `accessible` que apunte a `private` y compruebe si Cowork lo sigue. En PowerShell como administrador: `New-Item -ItemType Junction -Path "...\accessible\atajo" -Target "...\private"`.
- **Qué pasa si el MCP se cae.** Cierre el proceso de Node a mitad de sesión y observe **qué mensaje ve usted**. Importa porque una usuaria no técnica no debe quedarse sin saber que el sistema perdió su Core.

---

## Lo que NO debe hacer

- **No adjunte `experimental-root` entera ni `private`.** Invalidaría toda la prueba.
- **No use datos reales** de ningún expediente. Los archivos de prueba son texto inventado.
- **No deje el servidor registrado** al terminar.
- **No concluya de un solo intento.** Si algo se comporta raro, repítalo y anote ambas veces: una diferencia entre dos ejecuciones es en sí misma un hallazgo.
