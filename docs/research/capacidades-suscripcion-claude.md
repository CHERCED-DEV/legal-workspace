# Qué ofrece realmente la suscripción de Claude — inventario verificado

> **Propósito.** Los dueños pidieron *«usar todo lo que tenga Claude a disposición... que se conecte con su OneDrive, que le permita hacer cosas de Office y demás herramientas de trabajo»*. Antes de diseñar sobre esas capacidades hay que saber **cuáles existen de verdad, en qué plan y con qué requisitos**. Este documento solo registra lo comprobado; el diseño va en `technical-design/v0/19-integraciones-y-herramientas.md`.
>
> **Fecha de verificación: 2026-08-25.** La documentación de plataforma cambia; este inventario caduca. Cualquier decisión que dependa de una fila de estas tablas debe re-verificarse antes de implementar.
>
> **Método.** Consulta directa de páginas oficiales (`claude.com/docs`, `support.claude.com`) más observación directa del entorno de esta sesión. Nada aquí procede de blogs, foros ni memoria del modelo.

---

## 0. Los tres hallazgos que cambian el plan

Antes de las tablas, lo que un lector con prisa necesita saber:

1. **RIESGO ALTO — el conector de Microsoft 365 exige cuenta corporativa, no personal.** Está disponible en todos los planes, pero requiere *«una cuenta Microsoft de trabajo o de estudios en un tenant de Microsoft Entra»* y **excluye explícitamente las cuentas personales** (`outlook.com`, `hotmail.com`, `live.com`). Además exige que **un Administrador Global de Entra conceda consentimiento de tenant**, incluso en planes Free/Pro/Max. Si el OneDrive de la profesional es personal —lo habitual en ejercicio independiente— **este conector no se puede activar**, y ninguna suscripción de Claude lo arregla. Es un requisito del lado de Microsoft.
2. **HALLAZGO POSITIVO — el complemento de Word es probablemente lo más valioso de todo el inventario para ella, y estaba fuera del radar del proyecto.** *Claude para Word* se instala desde Microsoft AppSource, funciona con **Pro o Max** (no requiere plan de empresa), **no requiere administrador de Entra** para instalación individual, y hace exactamente el trabajo de una abogada: leer un documento abierto con citas por sección, editar en **modo control de cambios** revisable en el panel nativo de Word, trabajar los comentarios uno por uno, y resumir el redlining de la contraparte.
3. **RIESGO — la vía de instalación de nuestro MCP local no está confirmada para su plan.** La documentación de *Desktop Extensions / MCPB* dice literalmente *«Disponible para planes Team y Enterprise con Claude Desktop»*, mientras que el artículo de soporte sobre servidores MCP locales describe la instalación desde `Configuración > Extensiones` sin restringir plan, y la tabla de disponibilidad de plataformas dice que Cowork tiene *«soporte completo de MCP y plugins»*. **Las tres afirmaciones no son consistentes entre sí.** Esto es previo a B-04: antes de preguntar *si un MCP local alcanza rutas fuera de las carpetas adjuntas*, hay que saber **si ella puede instalar un MCP local en absoluto**.

---

## A. Conectores de almacenamiento

| Capacidad | Estado | Plan / superficie | Qué permite exactamente | Fuente |
|---|---|---|---|---|
| **Conector Microsoft 365** (SharePoint, OneDrive, Outlook, Teams) | **VERIFICADO — existe** | *«Disponible en todos los planes: Free, Pro, Max, Team y Enterprise.»* En Team/Enterprise un Owner debe habilitarlo primero | Buscar y analizar documentos en SharePoint y OneDrive; acceder a hilos de Outlook; revisar calendario de Teams; leer chats de Teams | [docs](https://claude.com/docs/connectors/microsoft/365) |
| — **requisito de cuenta** | **VERIFICADO — RESTRICTIVO** | — | *«Una cuenta Microsoft de trabajo o de estudios en un tenant de Microsoft Entra (las cuentas personales como outlook.com, hotmail.com o live.com no están soportadas)»* | [docs](https://claude.com/docs/connectors/microsoft/365) · [soporte](https://support.claude.com/en/articles/12542951-set-up-the-microsoft-365-connector) |
| — **requisito de administrador** | **VERIFICADO — RESTRICTIVO** | Aplica también en Free/Pro/Max | *«Un Administrador Global de Microsoft Entra todavía necesita conceder el consentimiento de tenant, por única vez»* | [docs](https://claude.com/docs/connectors/microsoft/365) |
| — **escritura en OneDrive** | **INCONCLUSIVE — la documentación oficial se contradice** | Requiere aprobación adicional del administrador de Entra y activación por la organización | La página de docs dice *«crear y actualizar archivos en SharePoint»* (solo SharePoint) en dos lugares distintos; el artículo de soporte dice *«crear y actualizar archivos en OneDrive y SharePoint»*. **No damos por buena la escritura en OneDrive** | [docs](https://claude.com/docs/connectors/microsoft/365) vs. [soporte](https://support.claude.com/en/articles/12542951-set-up-the-microsoft-365-connector) |
| — modelo de permisos | VERIFICADO | — | Delegados: *«Claude actúa en nombre del usuario y solo puede acceder y modificar contenido al que usted ya tiene permiso»* | [docs](https://claude.com/docs/connectors/microsoft/365) |
| **Integración de Google Drive** (la documentada) | **VERIFICADO — mucho más limitada de lo que suena** | Pro, Max, Team, Enterprise | **Solo Google Docs**, hasta 10 MB, **solo extracción de texto**. Google Sheets **no soportado**. Google Slides **no soportado**. Imágenes y comentarios **no se extraen**. Es para *aportar contexto*, no un sistema de archivos | [docs](https://claude.com/docs/connectors/google/drive) |
| **Conector de Google Drive con herramientas de escritura** | **OBSERVADO DIRECTAMENTE en esta sesión — plan y generalidad desconocidos** | Superficie: esta sesión. **No sabemos si está en el plan de ella** | Presenta herramientas de búsqueda estructurada, lectura, descarga, metadatos y permisos, **y también creación, actualización, copia, compartición y envío a papelera**. Es un mecanismo **distinto** de la integración documentada arriba | Observación del entorno, 2026-08-25. Sin página oficial localizada |
| **Conector dedicado de OneDrive** (independiente de M365) | **NOT FOUND** | — | No existe como conector separado en la documentación consultada. OneDrive solo aparece dentro del conector de Microsoft 365, con sus requisitos | [docs](https://claude.com/docs/connectors/overview) |

> **RIESGO documentado.** Que el conector conceda *«solo lo que usted ya puede ver»* es una garantía sobre **permisos**, no sobre **relevancia**. Un OneDrive profesional contiene material de **todos** sus casos. Un conector así, activo durante el trabajo en un expediente, puede traer a la conversación material de un caso distinto sin que nadie lo haya pedido. Eso no es un fallo del conector: es la consecuencia de conectar un almacén general a un trabajo particular, y hay que diseñarlo, no descubrirlo.

---

## B. Documentos de Office — hay **dos** mecanismos distintos, y conviene no confundirlos

### B.1 Creación de archivos desde la conversación

| Capacidad | Estado | Plan / superficie | Qué permite exactamente | Fuente |
|---|---|---|---|---|
| Crear `.docx`, `.xlsx`, `.pptx`, `.pdf` | **VERIFICADO** | *«Free, Pro, Max: activado por defecto. Team y Enterprise: activado por defecto, los owners pueden desactivarlo.»* Web, Claude Desktop y móvil | Genera documentos de Word, hojas de Excel con fórmulas funcionales, presentaciones y PDF, descargables | [soporte](https://support.claude.com/en/articles/12111783-create-and-edit-files-with-claude) |
| Límite de tamaño | VERIFICADO | — | *«El tamaño máximo es 30 MB por archivo, tanto para subidas como para descargas.»* PDF por encima de 30 MB pueden procesarse sin cargarse al contexto | [soporte](https://support.claude.com/en/articles/12111783-create-and-edit-files-with-claude) |
| Entrega del archivo | VERIFICADO | — | Descarga directa desde la conversación, o **guardar directamente en Google Drive**. **Guardar en OneDrive: NOT FOUND** | [soporte](https://support.claude.com/en/articles/12111783-create-and-edit-files-with-claude) |
| Activación | VERIFICADO | — | `Configuración > Capacidades >` interruptor de ejecución de código y creación de archivos | [soporte](https://support.claude.com/en/articles/12111783-create-and-edit-files-with-claude) |
| Aviso de seguridad del propio fabricante | **VERIFICADO — relevante para nosotros** | — | Se ejecuta en *«un contenedor aislado, en sandbox»*, y se advierte que **mediante inyección de instrucciones Claude podría ser engañado para enviar datos a servidores externos si el acceso de red está habilitado**. Desactivar el acceso de red es una opción **solo de Team/Enterprise** | [soporte](https://support.claude.com/en/articles/12111783-create-and-edit-files-with-claude) |

### B.2 Complementos de Office — **Claude para Word, Excel, PowerPoint y Outlook**

Mecanismo completamente distinto: un **complemento (add-in) que corre dentro de la aplicación de Office**, no un conector en la nube.

| Capacidad | Estado | Plan / superficie | Qué permite exactamente | Fuente |
|---|---|---|---|---|
| **Claude para Word** | **VERIFICADO** | *«Disponible de forma general para los planes Pro, Max, Team y Enterprise.»* **Free queda fuera** | Ver detalle abajo | [docs](https://claude.com/docs/office-agents/word) |
| — versiones soportadas | VERIFICADO | Word en la web; **Word en Windows con suscripción a Microsoft 365**, versión 2205 build 15202.10000 o posterior; Word en Mac 16.61 build 22040100 o posterior | **No funciona** en Word 2016/2019 perpetuo o por volumen, ni en iPad, ni en Android. **Archivos `.doc` heredados no soportados**: hay que guardar como `.docx` | [docs](https://claude.com/docs/office-agents/word) |
| — instalación individual | **VERIFICADO — sin administrador** | — | Desde el listado *Claude for Microsoft 365* en Microsoft AppSource, y se inicia sesión **con la cuenta de Claude**. **No aparece requisito de Administrador de Entra para la instalación individual** | [docs](https://claude.com/docs/office-agents/word) |
| — qué hace, en concreto | VERIFICADO | — | Preguntar sobre el documento con **citas por sección clicables**; editar el texto seleccionado preservando estilos y numeración; **modo control de cambios**, donde cada edición aparece como revisión aceptable o rechazable en el panel de revisión nativo de Word; trabajar hilos de comentarios editando el texto anclado y respondiendo qué cambió; **resumir el redlining de la contraparte** y señalar qué revisiones merecen discusión; rellenar plantillas con los estilos del documento; navegación semántica por temas | [docs](https://claude.com/docs/office-agents/word) |
| — alcance de lectura | **VERIFICADO — acotado, y eso es bueno** | — | *«Claude lee el contenido del documento que usted tiene abierto, incluyendo texto, comentarios, cambios controlados, notas al pie, tablas y marcadores. Solo accede al documento que usted tiene abierto en Word.»* | [docs](https://claude.com/docs/office-agents/word) |
| — limitaciones declaradas | **VERIFICADO — leer literalmente** | — | *«Claude solo puede leer y escribir en archivos que estén actualmente abiertos... Claude no puede crear, abrir, cerrar ni cambiar de archivo directamente.»* Y no se recomienda para *«presentaciones judiciales o documentos críticos para auditoría sin verificación»* ni para *«sustituir el juicio jurídico o financiero»* | [docs](https://claude.com/docs/office-agents/word) · [cross-app](https://claude.com/docs/office-agents/work-across-apps) |
| — **advertencia de inyección de instrucciones** | **VERIFICADO — crítica para este caso de uso** | — | *«Use Claude para Word solo con documentos de confianza. Documentos de fuentes externas como plantillas descargadas, archivos de la contraparte o archivos compartidos por correo pueden contener instrucciones ocultas»* que manipulen el complemento para extraer datos, modificar contenido crítico como cláusulas contractuales o cifras, o ejecutar acciones destructivas | [docs](https://claude.com/docs/office-agents/word) |
| — dónde queda el historial | VERIFICADO | — | El historial de chat se guarda **localmente en el navegador (IndexedDB)**, no en servidores de Anthropic, y no se sincroniza entre dispositivos. Entradas y salidas se borran del backend **en 30 días** | [docs](https://claude.com/docs/office-agents/word) |
| — no hereda retención de la organización | VERIFICADO | — | *«Claude para Word no hereda la configuración personalizada de retención de datos que su organización pudiera tener. La actividad no se incluye en los registros de auditoría de Enterprise ni en la Compliance API»* | [docs](https://claude.com/docs/office-agents/word) |
| **Trabajo entre aplicaciones de M365** | VERIFICADO | *«Un plan de pago de Claude: Pro, Max, Team o Enterprise.»* Requiere los **cuatro** complementos instalados y activados una vez | Leer de Excel y escribir en Word, etc., **sobre archivos abiertos**. En Pro y Max el interruptor viene activado por defecto; es **por dispositivo** | [docs](https://claude.com/docs/office-agents/work-across-apps) |
| **Claude para Excel / PowerPoint / Outlook** | VERIFICADO — existen | Pro, Max, Team, Enterprise | Complementos hermanos, instalados igual desde AppSource. Detalle no verificado en profundidad en esta pasada | [docs](https://claude.com/docs/office-agents/work-across-apps) |
| **Skills dentro de los complementos** | **VERIFICADO — muy relevante** | — | *«Las Skills que usted haya habilitado en la configuración de Claude aplican cuando Claude está trabajando en Excel, PowerPoint, Word u Outlook.»* Es decir, **`fact-builder` podría aplicar dentro de Word** | [docs](https://claude.com/docs/office-agents/work-across-apps) |

> **La advertencia de inyección merece detenerse.** El fabricante advierte contra usar el complemento *«con documentos que no sean de confianza... archivos de la contraparte»*. Para un abogado litigante, **leer los documentos de la contraparte no es un caso límite: es el trabajo**. Esto no descalifica la herramienta, pero obliga a que el trabajo con material adverso ocurra con el modo de control de cambios activo y revisión humana de cada revisión — y a no delegarle acciones no supervisadas sobre ese material.

---

## C. Cowork y la vía de instalación de nuestro MCP

| Capacidad | Estado | Plan / superficie | Qué permite exactamente | Fuente |
|---|---|---|---|---|
| **Qué es Cowork** | VERIFICADO | Dentro de Claude Desktop | *«Usa la misma arquitectura agéntica que impulsa Claude Code, accesible dentro de Claude Desktop sin abrir la terminal.»* *«Trabaja directamente en su computador: Claude lee y escribe archivos locales sin necesidad de subidas ni descargas manuales.»* | [docs](https://claude.com/docs/cowork/overview) |
| **Plan requerido para Cowork** | **NOT FOUND** en la página de overview | — | La página no declara requisito de plan. **POR VERIFICAR** antes de comprometer nada | [docs](https://claude.com/docs/cowork/overview) |
| **Cowork no hereda la configuración de Claude Code** | **VERIFICADO — confirma el hallazgo del spike** | — | *«Cowork carga los que estén habilitados para su cuenta de claude.ai, sincronizados al inicio de la sesión, y no lee el directorio `~/.claude` del CLI de Claude Code. Para usar una skill o un plugin que solo existe en `~/.claude`, añádalo en Customize.»* | [docs](https://claude.com/docs/cowork/overview) |
| **Disponibilidad de MCP por superficie** | VERIFICADO | — | *«Claude Desktop — soporte completo de MCP y extensiones de escritorio locales.»* *«Claude Cowork — soporte completo de MCP y de plugins.»* | [docs](https://claude.com/docs/connectors/overview) |
| **Plugins como vehículo de un MCP local** | **VERIFICADO — vía candidata para nuestro producto** | *«Están disponibles en Claude Code y Cowork.»* | *«Los plugins combinan conectores MCP, Skills, comandos y sub-agentes en paquetes de capacidades compartibles.»* Y para distribuir un servidor local: *«empaquételo como MCPB... o inclúyalo en un plugin usando `.mcp.json`»* | [docs](https://claude.com/docs/connectors/overview) · [plugins](https://claude.com/docs/plugins/overview) |
| **Desktop Extensions / MCPB** | **INCONCLUSIVE — CONTRADICCIÓN EN LA DOCUMENTACIÓN** | La página de docs dice *«Disponible para planes Team y Enterprise con Claude Desktop»*; el artículo de soporte describe la instalación desde `Configuración > Extensiones` sin mencionar restricción de plan | Servidores MCP locales que corren en el dispositivo del usuario, empaquetados con dependencias y firma de código | [docs](https://claude.com/docs/connectors/custom/desktop-extensions) vs. [soporte](https://support.claude.com/en/articles/10949351-getting-started-with-local-mcp-servers-on-claude-desktop) |
| **Configuración manual por archivo JSON de Claude Desktop** | VERIFICADO — existe como vía | Claude Desktop. **Si aplica a Cowork: POR VERIFICAR** | Se configura un archivo JSON que indica qué servidores arrancar; Claude Desktop los inicia al lanzarse | [soporte](https://support.claude.com/en/articles/10949351-getting-started-with-local-mcp-servers-on-claude-desktop) |
| **Los conectores remotos NO corren en la máquina de ella** | **POR VERIFICAR — indicio fuerte, sin fetch directo** | — | Un resumen de búsqueda oficial indica que Claude conecta con servidores MCP remotos *desde la infraestructura en la nube de Anthropic, no desde el dispositivo local*. Si se confirma, **un MCP remoto no puede tocar su disco**, y la vía local es la única posible para nuestro Core | Pendiente: fetch directo de [remote-mcp](https://claude.com/docs/connectors/custom/remote-mcp) |
| **Conectores instalados en esta sesión** | OBSERVADO | — | El registro de conectores devolvió **vacío**: no hay conectores instalados en este entorno. La búsqueda del registro por «onedrive, microsoft, office» devolvió **cero resultados** | Observación del entorno, 2026-08-25 |

---

## D. Correo y calendario

| Capacidad | Estado | Plan / superficie | Qué permite | Fuente |
|---|---|---|---|---|
| Outlook (correo y calendario) | VERIFICADO | Dentro del conector M365 — **con sus mismos requisitos de cuenta corporativa y administrador** | Buscar hilos y correo archivado; enviar y gestionar correo; crear, actualizar y eliminar eventos. **No puede adjuntar archivos a los borradores que crea** | [docs](https://claude.com/docs/connectors/microsoft/365) |
| Gmail y Google Calendar | VERIFICADO — existen como integraciones | Página específica no verificada en esta pasada | — | [docs](https://claude.com/docs/connectors/overview) |
| Complemento **Claude para Outlook** | VERIFICADO — existe | Pro, Max, Team, Enterprise | Trabaja sobre **el correo o evento actualmente abierto** | [docs](https://claude.com/docs/office-agents/work-across-apps) |

> **SUPUESTO no verificado y consecuencia práctica:** si su correo profesional está en Gmail o en un proveedor propio —lo más común en el ejercicio independiente en Colombia—, todo el bloque de Outlook es irrelevante y no debe presentarse como parte de la propuesta.

---

## E. Qué se puede aprovechar, qué exige más plan, y qué no existe

### E.1 Aprovechable ya, sin requisitos externos

| Capacidad | Plan mínimo verificado | Por qué importa aquí |
|---|---|---|
| Creación de `.docx`, `.xlsx`, `.pptx`, `.pdf` desde la conversación | **Free** | Es la vía para entregarle borradores y tablas sin depender de ningún conector |
| Skills | Disponibles en Cowork vía `Customize` | Es donde vive `fact-builder`. **No requiere infraestructura** |
| Cowork leyendo y escribiendo archivos locales | Plan **POR VERIFICAR** | Es el fundamento del diseño entero: el material no se sube, se lee donde está |

### E.2 Exige plan de pago (Pro o Max bastan)

| Capacidad | Plan mínimo | Requisito adicional |
|---|---|---|
| **Claude para Word** (y Excel, PowerPoint, Outlook) | **Pro** | Suscripción a Microsoft 365 para la versión de escritorio en Windows; instalación desde AppSource. **Sin administrador de Entra** |
| Trabajo entre aplicaciones de M365 | **Pro** | Los cuatro complementos instalados y activados al menos una vez |
| Integración documentada de Google Drive | **Pro** | Solo Google Docs, solo texto |

### E.3 Exige algo que **no depende del plan de Claude** — y puede ser inalcanzable

| Capacidad | Qué exige | Probabilidad de que ella lo tenga |
|---|---|---|
| **Conector de Microsoft 365 (OneDrive, SharePoint, Outlook, Teams)** | Cuenta Microsoft **de trabajo o estudios en un tenant de Entra** + consentimiento de un **Administrador Global de Entra** | **POR VERIFICAR — y es la pregunta más urgente del inventario.** En ejercicio independiente con OneDrive personal, **no se puede activar en absoluto** |
| Escritura en OneDrive desde el conector | Lo anterior + aprobación adicional de permisos de escritura + activación por la organización | Menor aún. Y la documentación **se contradice** sobre si la escritura llega a OneDrive o solo a SharePoint |
| Desactivar el acceso de red del sandbox de ejecución | Plan **Team o Enterprise** | Fuera del alcance de un plan individual |

### E.4 Lo que **no existe** y no hay que prometer

| Lo que no hay | Estado |
|---|---|
| Conector de OneDrive independiente del de Microsoft 365 | **NOT FOUND** |
| Guardar archivos generados directamente en OneDrive | **NOT FOUND** — solo se documenta descarga y guardado en Google Drive |
| Soporte de Google Sheets o Google Slides en la integración documentada de Drive | **VERIFICADO que NO** |
| Soporte de cuentas Microsoft personales en el conector M365 | **VERIFICADO que NO** |
| Claude para Word creando, abriendo o cambiando de archivo por su cuenta | **VERIFICADO que NO** — solo trabaja sobre el archivo abierto |
| Que un conector convierta material externo en prueba del expediente | **No es cuestión de plataforma: lo prohíbe ADR-006.** Ningún conector, de ningún plan, cambia esto |

---

## F. Lo que hay que verificar antes de comprometer nada

| # | Pregunta | Por qué bloquea | Cómo se resuelve |
|---|---|---|---|
| V-1 | **¿Su OneDrive es de cuenta personal o de una cuenta corporativa en Entra?** | Decide si todo el bloque de Microsoft 365 es viable o inalcanzable. **Es la pregunta más barata y de mayor impacto del inventario** | Preguntarle con qué correo entra a OneDrive |
| V-2 | ¿Qué plan de Claude tiene? | Separa lo disponible hoy de lo que exige actualizar | Preguntar |
| V-3 | ¿Tiene suscripción a Microsoft 365, y qué versión de Word? | Decide si el complemento de Word —la capacidad más valiosa localizada— es instalable | Ver la versión en Word: *Archivo > Cuenta* |
| V-4 | **¿Puede instalarse un MCP local en su plan y en Cowork, y por qué vía —plugin con `.mcp.json`, MCPB, o configuración manual?** | Contradicción documental sin resolver. **Es previo a B-04** | Prueba empírica desde su Cowork |
| V-5 | ¿Un conector remoto puede alcanzar el disco local? | Si la respuesta es no, la vía local es la única y no hay alternativa | Fetch directo de la página de MCP remoto |
| V-6 | ¿Qué plan requiere Cowork? | El diseño entero lo presupone disponible | La página no lo declara; verificar en la aplicación |

---

## G. Fuentes consultadas

| Documento | URL |
|---|---|
| Conector Microsoft 365 (docs) | https://claude.com/docs/connectors/microsoft/365 |
| Configurar el conector Microsoft 365 (soporte) | https://support.claude.com/en/articles/12542951-set-up-the-microsoft-365-connector |
| Crear y editar archivos con Claude (soporte) | https://support.claude.com/en/articles/12111783-create-and-edit-files-with-claude |
| Claude para Word (docs) | https://claude.com/docs/office-agents/word |
| Trabajo entre aplicaciones de M365 (docs) | https://claude.com/docs/office-agents/work-across-apps |
| Visión general de Cowork (docs) | https://claude.com/docs/cowork/overview |
| Visión general de conectores (docs) | https://claude.com/docs/connectors/overview |
| Extensiones de escritorio / MCPB (docs) | https://claude.com/docs/connectors/custom/desktop-extensions |
| Integración de Google Drive (docs) | https://claude.com/docs/connectors/google/drive |
| Servidores MCP locales en Claude Desktop (soporte) | https://support.claude.com/en/articles/10949351-getting-started-with-local-mcp-servers-on-claude-desktop |
