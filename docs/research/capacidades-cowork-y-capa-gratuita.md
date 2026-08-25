# Capacidades de Cowork y de la capa gratuita — inventario único

**Fecha de verificación: 2026-08-25.**
**Método:** cinco verificadores recorrieron la documentación oficial (dominios: planes, cowork, herramientas, skills, alternativa) y tres refutadores adversariales independientes intentaron tumbar cada afirmación de gratuidad. Este documento consolida ambos pases. **El veredicto adversarial manda sobre la afirmación original.**

**Regla de lectura.** Cada fila lleva etiqueta y URL. Sin fuente, la fila no existe: no se ha completado ninguna tabla por simetría ni por inferencia.

| Etiqueta | Significado |
|---|---|
| **VERIFICADO** | Cita literal en fuente oficial, y ningún refutador la tumbó. |
| **REFUTADO** | Un refutador la tumbó con fuente. **No se presenta como disponible.** |
| **DUDOSO** | Sobrevivió a medias, o los refutadores discrepan entre sí. Se aplica la lectura más restrictiva. |
| **INCONCLUSIVE** | Dos o más páginas oficiales se contradicen y no hay árbitro documental. |
| **NOT FOUND** | Se buscó y no existe página oficial que lo declare. La ausencia no es permiso. |
| **POR VERIFICAR** | Solo se resuelve empíricamente en la cuenta o el equipo de ella. |

> **AVISO DE CADUCIDAD.** Todo lo de aquí es una fotografía del 2026-08-25. Los planes, precios, límites y disponibilidad por superficie cambian sin preaviso — la propia página de precios lo dice: *"Price and plans are subject to change at Anthropic's discretion."* Varias funciones citadas están declaradas **beta** o **research preview**, etiquetas con las que el proveedor se reserva cambiarlas o retirarlas. **Este inventario debe reverificarse antes de cualquier decisión de gasto y antes de comprometer un diseño.** Ninguna fila autoriza a prometer una capacidad sin comprobarla en la cuenta y el equipo reales.

---

## §0 — Los hallazgos que cambian el plan

### La pregunta decisiva: ¿en qué plan está Cowork?

**Cowork está en los planes de pago. No existe en el plan gratuito.** [VERIFICADO]

Tres páginas oficiales independientes coinciden, y los tres refutadores lo dieron por sostenido sin encontrar ninguna grieta. Es la conclusión más sólida de todo el inventario y la única que puede darse por cerrada sin prueba empírica.

- Centro de ayuda: *"Paid Claude subscription: Cowork is available to paid Claude plans (Pro, Max, Team, Enterprise) only."* — https://support.claude.com/en/articles/13345190-get-started-with-claude-cowork
- Página de producto: *"Works with a paid plan."* — https://claude.com/product/cowork
- Página de precios: *"Includes Claude Cowork"* aparece como viñeta de **Pro**, dentro del bloque "Everything in Free, plus". No aparece en la lista del plan Free. — https://claude.com/pricing

**Consecuencia directa para el encargo: la exigencia de "una alternativa sin costo que funcione" NO es realizable sobre Cowork.** Todo el diseño del proyecto presupone Cowork leyendo y escribiendo el expediente en disco. Ese presupuesto tiene precio: **200 USD al año pagados por adelantado (17 USD/mes), o 20 USD/mes**, más impuestos.

Y no hay puerta trasera. Con Cowork caen, todos verificados como de pago: **Claude Code** (Pro/Max), **plugins** (todos los planes de pago), **sub-agentes y hooks** (solo corren en Cowork), **Dispatch** (Pro/Max), **tareas programadas** (planes de pago), **computer use** (Pro/Max, research preview), **live artifacts** (planes de pago) y **Claude en Chrome** (planes de pago). **En el plan gratuito no existe ninguna vía agéntica de lectura y escritura sobre archivos locales.**

### Por qué el proyecto llegó hasta aquí creyendo lo contrario

La página de documentación sobre la que se apoyó el diseño, https://claude.com/docs/cowork/overview.md, **no declara requisito de plan en ninguna línea de su texto**. Ni Free, ni Pro, ni la palabra suscripción. Un lector que se guíe solo por ella concluye, erróneamente, que Cowork podría estar disponible sin costo. Esto resuelve la pregunta V-6 del inventario previo y explica el origen del supuesto.

### Los otros cinco hallazgos que cambian el plan

**1. Pagar Pro no garantiza Cowork en su equipo.** [VERIFICADO — riesgo alto, ella usa Windows 11]
*"Claude Desktop for Windows requires the Virtual Machine Platform to use Cowork."* Es una característica opcional de Windows que exige permisos de administrador local para activarse, y el changelog reconoce que existen *"Windows machines that can't run local Cowork"*. **Hay que verificarlo en su máquina ANTES de recomendar el gasto.** — https://support.claude.com/en/articles/12622703-deploy-claude-desktop-for-windows

**2. Las sesiones de Cowork corren en la nube por defecto: el expediente sale del dispositivo.** [VERIFICADO — riesgo de confidencialidad]
*"Cowork sessions run in the cloud by default: the agent loop and code execution run on Anthropic's servers"* y *"The agent's work, including any local files it opens through the desktop app, is processed on Anthropic's servers rather than staying on the device."* Esto va justo en contra del relato "el material no se sube, se lee donde está". El interruptor "Run Cowork in the cloud" solo se documenta como control de administrador en Team y Enterprise; **para Pro y Max no se localizó control equivalente**. Además, *"Local MCP servers don't run in sessions in the cloud"*: si nuestro Core corre como MCP local y la sesión es en la nube, no funciona. — https://support.claude.com/en/articles/14479288-claude-cowork-architecture-overview

**3. El dolor número uno declarado por la profesional no tiene solución en la plataforma.** [NOT FOUND]
**No existe transcripción de archivos de audio subidos.** Ningún formato de audio figura en la lista oficial de tipos admitidos, y no se localizó ninguna página que documente subir y transcribir una grabación en claude.ai, Cowork o Desktop. El dictado y el modo voz capturan **habla en vivo**, no grabaciones. Una entrevista grabada habría que transcribirla fuera y solo entonces entra al flujo. **Hay que decírselo antes de que construya expectativas.** — https://support.claude.com/en/articles/8241126-upload-files-to-claude

**4. Sobre expedientes escaneados, la trazabilidad a folio está oficialmente negada.**
*"As image citations are not yet supported, PDFs that are scans of documents and do not contain extractable text are not citable."* Y la función de citas con número de página se documenta para la Claude API, AWS, Bedrock, Google Cloud y Microsoft Foundry — **claude.ai no figura**. Leer un escaneado y citar el folio exacto son cosas distintas: lo segundo no es una capacidad de la suscripción. — https://platform.claude.com/docs/en/build-with-claude/citations

**5. El plan gratuito no tiene cifras publicadas, y su cuota es elástica a la baja.** [NOT FOUND + VERIFICADO]
No existe ninguna página oficial que publique cuántos mensajes, tokens o páginas permite Free, ni cuál es su ventana de contexto (la cifra de 1M/500K/200K se atribuye expresamente a *"paid plans"*). Lo que sí consta: Pro da *"at least five times the usage per session compared to our free service"*, y Anthropic se reserva encoger la cuota gratuita — *"the number of messages you can send will vary based on demand, and we may impose other types of usage limits"*. **Cualquier cifra que le demos sobre cuánto rinde Free sería inventada.** — https://support.claude.com/en/articles/11647753-how-do-usage-and-length-limits-work · https://support.claude.com/en/articles/8114491-get-started-with-claude

---

## §1 — La línea del costo cero

Esta es la respuesta directa a los dueños. Tres columnas: lo que funciona gratis y sobrevivió a los tres refutadores; lo que parecía gratis y fue tumbado o quedó dudoso; y lo que exige pago, con la cifra.

### 1.A — Funciona gratis y sobrevivió a la refutación

| Capacidad | Etiqueta | Límite real que hay que declarar junto a la promesa | Fuente |
|---|---|---|---|
| **Ejecución de código y creación de archivos** (.docx, .xlsx con fórmulas, .pptx, .pdf) — *"available to all Claude users (Free, Pro, Max, Team, and Enterprise)"* | VERIFICADO (3/3 sostienen) | **Viene APAGADO por defecto**: hay que activarlo en Settings > Capabilities. 30 MB por archivo, subida y descarga. Y **gasta más cuota que chatear**: *"creating files will use more of your limit compared to normal chats"*. | https://support.claude.com/en/articles/12111783-create-and-edit-files-with-claude |
| **Artifacts** (Markdown editable por selección, tablas, líneas de tiempo, diagramas) | VERIFICADO (3/3) | Depende del mismo interruptor: *"We no longer support artifacts without Code execution and file creation enabled"*. Y **consume cuota**: la guía de límites enumera *"Artifact creation and usage"* entre los factores que la agotan. | https://support.claude.com/en/articles/9487310-what-are-artifacts-and-how-do-i-use-them |
| **Memoria entre conversaciones, activada por defecto**, con espacio de memoria **separado por proyecto** | VERIFICADO (3/3) | Activada por defecto es también un riesgo: datos de un cliente persisten sin que ella lo pida. **Buscar en chats pasados es de pago.** No hay límite de tamaño publicado para la memoria. | https://support.claude.com/en/articles/11817273-use-claude-s-chat-search-and-memory-to-build-on-previous-context |
| **Cinco proyectos** — *"Free users can create a maximum of five projects."* | VERIFICADO (3/3, el número) | Cinco es el techo duro. **Sin el RAG de planes de pago**, todo el conocimiento del proyecto debe caber crudo en una ventana de contexto cuyo tamaño en Free no está publicado. Archivos de proyecto: 30 MB, no los 500 MB del chat. | https://support.claude.com/en/articles/9517075-what-are-projects |
| **Aplicación de escritorio para Windows, en modo chat** | VERIFICADO (3/3) | Windows 10 o superior. **Instalarla NO añade cuota**: *"your usage of all different Claude product surfaces… counts towards the same usage limit"*. Free = solo Chat; Code y Cowork no están. | https://support.claude.com/en/articles/10065433-install-claude-desktop |
| **UN (1) conector personalizado por MCP remoto** — *"Free users are limited to one custom connector."* | VERIFICADO (3/3) | **Uno solo**: el Core tendría que caber entero en un servidor. Es **remoto**: *"Claude connects to your remote MCP server from Anthropic's cloud infrastructure, rather than from your local device"* — **no toca su disco**. Exige alojamiento accesible desde internet público (costo propio). La autenticación por cabeceras está en beta restringida: *"contact Anthropic for early access"*. | https://support.claude.com/en/articles/11175166-get-started-with-custom-connectors-using-remote-mcp |
| **Exportación de los datos propios** — *"available to individual Claude users on Free, Pro, and Max plans"* | VERIFICADO (2/3 sostienen; el tercero no la releyó) | No se puede lanzar desde iOS ni Android. El enlace de descarga **expira a las 24 horas**. | https://support.claude.com/en/articles/9450526-export-your-claude-data |
| **Importar, ver y editar la propia memoria** — *"available for Free, Pro, Max, and Team plans"* | VERIFICADO (2/3; el tercero objeta que "experimental" es barrera) | Declarado **experimental**: *"Claude may not always successfully incorporate imported memories"*. No sirve como mecanismo fiable de portabilidad. | https://support.claude.com/en/articles/12123587-import-and-export-your-memory-from-claude |
| **Modo voz** — *"a beta feature available to all plans (Free, Pro, Max, Team, and Enterprise)"* | VERIFICADO (3/3) | Beta. *"Support for languages other than English is in beta"* y el artículo **no publica lista de idiomas para voz**. Consume la misma cuota que el texto. | https://support.claude.com/en/articles/11101966-use-voice-mode |
| **Dictado** (habla → texto en el cuadro de mensaje), **español incluido** en la lista de doce idiomas | VERIFICADO (2/3; el tercero no lo releyó y duda de la calidad en español jurídico) | **Solo móvil**: *"when using Claude for iOS or Android"*. No existe en escritorio ni web, que es donde trabajaría los expedientes. | https://support.claude.com/en/articles/10065434-use-dictation-on-claude-mobile |
| **Interfaz en español (Latinoamérica y España)**, sin restricción de plan declarada | VERIFICADO (2/3; el tercero no lo releyó) | Cubre *"web and desktop applications"*. Idioma de interfaz ≠ calidad de salida en derecho colombiano. No existe función de traducción con garantías. | https://support.claude.com/en/articles/10769299-how-to-use-claude-in-your-preferred-language |
| **Publicar un artifact** — *"Publishing is available on Free, Pro, and Max plans."* | VERIFICADO como **riesgo, no como beneficio** | Es la única capacidad del inventario donde la gratuidad es el peligro. Lo hace **público**: *"Non-users: View and interact with any published artifact without signing up."* Y el remedio es destructivo: *"Once you unpublish an artifact, you cannot publish that same artifact again"* y *"Unpublishing also permanently deletes all associated storage data"*. Team y Enterprise **no pueden** publicar hacia afuera: la única protección corporativa es justo la que ella no tendrá. **Regla: no publicar nunca material de un caso.** | https://support.claude.com/en/articles/9547008-publish-and-share-artifacts |
| **Escribir un skill** (archivo `SKILL.md` de texto plano con frontmatter YAML, estándar abierto Agent Skills) | VERIFICADO (3/3) — **no depende de ningún plan** | Es la única pieza del proyecto independiente del proveedor: *"Skills you create can work across any platform adopting the standard."* Lo restringido es **ejecutarlo**, no escribirlo. Existe un límite de tamaño del ZIP al subirlo que la documentación invoca (*"ZIP file exceeds size limits"*) **sin publicar la cifra**. | https://claude.com/docs/skills/overview |

### 1.B — Parecía gratis, pero fue refutado o quedó dudoso

| Afirmación de gratuidad | Veredicto | Qué la tumbó | Fuente(s) |
|---|---|---|---|
| **Las Skills funcionan en el plan gratuito** | **DUDOSO — los refutadores discrepan** | Contradicción documental viva. La documentación técnica **excluye Free**: *"Skills are available for users on Pro, Max, Team, and Enterprise plans."* Tres artículos de soporte dicen lo contrario con la misma frase salvo la palabra Free. **Se buscó árbitro en la página de precios y no existe: "Skills" no aparece en ninguna viñeta, ni de Free ni de Pro.** Dos refutadores la dejan DUDOSA y aplican el sesgo restrictivo; **el tercero la da por resuelta a favor de Free**. Se aplica la lectura más restrictiva: **no se puede prometer**. Barrera adicional aunque se resolviera a favor: una skill en Free sería una plantilla de instrucciones, no lógica ejecutable — no podría empaquetarse como plugin (de pago) ni usar hooks ni sub-agentes (solo Cowork, de pago). | https://claude.com/docs/skills/overview vs https://support.claude.com/en/articles/12512180-use-skills-in-claude |
| **Los conectores web están disponibles para todos los usuarios, sin restricción de plan** | **REFUTADO** (el mecanismo existe; ningún conector útil es activable sola y gratis) | La frase de soporte es literal, pero enumera **superficies**, no reparte planes. Conector por conector: Gmail, Drive y Calendar dicen *"Available on Pro, Max, Team, and Enterprise plans"*; **Microsoft 365** exige tenant de Entra, Global Administrator y **rechaza cuentas personales**; **Slack** exige que un administrador del espacio de trabajo apruebe la app. Y el tutorial oficial abre con: *"Prerequisites: A Claude account (Pro, Max, Team, or Enterprise for most connectors)"* — cuarta fuente en contra, que nadie había encontrado. Un refutador la sostiene como frase literal; los otros dos la refutan en lo práctico. Gana la restrictiva. | https://claude.com/docs/connectors/getting-started.md · https://support.claude.com/en/articles/11176164-use-connectors-to-extend-claude-s-capabilities |
| **Conectores de Google Workspace (Drive, Gmail, Calendar) con lectura y ESCRITURA para todos los usuarios** | **REFUTADO** (2 refutadores lo tumban, 1 lo deja dudoso) | Cae por dos vías independientes. **(a) La escritura está negada en la propia documentación, con independencia del plan**: *"Claude cannot create, send, or modify emails"* y *"Claude cannot create, modify, or delete calendar events"*. **(b) El plan**: tres páginas de docs dicen *"Available on Pro, Max, Team, and Enterprise plans"*, más la línea de prerrequisitos del tutorial. Y aunque el plan se resolviera a favor, **el conector de Drive solo lee Google Docs**: Sheets NO, Slides NO, imágenes NO, comentarios NO, máximo 10 MB, solo extracción de texto — inservible para un expediente en .docx o una liquidación en .xlsx. | https://claude.com/docs/connectors/google/gmail.md · https://claude.com/docs/connectors/google/calendar.md · https://claude.com/docs/connectors/google/drive |
| **Extensiones de escritorio (MCPB) alcanzarían al plan gratuito, dando acceso local sin costo** | **DUDOSO / INCONCLUSIVE — es la prueba empírica de mayor valor pendiente** | Contradicción a tres bandas sin resolver (§7.2). Y **dos barreras que sobreviven aunque el plan se resuelva a favor**: (i) *"Local MCP servers distributed through third-party package registries like npm or PyPI cannot be listed directly in the Connectors Directory"* — no hay extensión de sistema de archivos instalable por autoservicio, alguien tiene que construirle y entregarle un `.mcpb`; (ii) **acceso a disco no es agencia**: Claude Desktop en Free es **solo chat**, sin bucle agéntico, sin hooks, sin sub-agentes, sin sesiones de fondo. Ganar acceso al disco no es ganar el Legal OS. A favor: Claude Desktop trae Node.js incorporado y la instalación es doble clic. | https://claude.com/docs/connectors/custom/desktop-extensions.md vs https://support.claude.com/en/articles/11176164-use-connectors-to-extend-claude-s-capabilities |
| **"Se pueden subir 20 archivos por chat de hasta 500 MB cada uno"** | **REFUTADO como promesa utilizable** | Las cifras están bien copiadas pero engañan: 20 × 500 MB son 10 GB y no existe ventana de contexto capaz de sostenerlo. Son topes del **ingestor**, no capacidad de trabajo. La guía de errores lo delata desde el otro lado: la solución oficial al exceso es *"Removing attachments or files"*. Agravante: los adjuntos **no se pagan una vez**, encarecen todos los mensajes posteriores — *"The number of messages you can send will vary based on message length, including the length of files you attach"*. Y dentro de un **proyecto** el tope real baja a **30 MB por archivo**. | https://support.claude.com/en/articles/8241126-upload-files-to-claude · https://support.claude.com/en/articles/8325606-what-is-the-pro-plan |
| **"El contenido cacheado en un proyecto no vuelve a contar contra el límite, y eso estira la cuota gratuita"** | **REFUTADO — la segunda mitad no tiene fuente en las páginas de proyectos** | Los cinco proyectos sostienen; la ventaja de caché **no aparece en ninguna de las dos páginas de proyectos** consultadas. Y aunque existiera, es irrelevante: el mecanismo que hace grande a un proyecto es de pago — *"Claude seamlessly enables RAG mode to expand capacity by up to 10x"*, y esa mejora *"is only available to users with paid Claude plans"*. El proyecto gratuito es una caja **diez veces menor**. | https://support.claude.com/en/articles/9517075-what-are-projects |
| **"La búsqueda web funciona en cuentas gratuitas, con cupo diario"** | **DUDOSO — los refutadores discrepan sobre el plan** | El artículo citado **no declara plan alguno**: no menciona Free en ninguna parte, y la única habilitación que describe es la de administradores Team/Enterprise. El único apoyo para "funciona en Free" es la viñeta comercial de la página de precios. Lo que sí está citado literalmente es el consumo: *"Usage of web search and web fetch counts toward your daily limits."* No hay ninguna cifra publicada de cuántas búsquedas. | https://support.claude.com/en/articles/10684626-enable-and-use-web-search · https://claude.com/pricing |
| **"Subir y analizar PDF de hasta 1000 páginas (visual hasta 100) no está restringido por plan"** | **DUDOSO** (3/3 refutadores) | El silencio sobre planes no es permiso. Y las 1000 páginas son límite del ingestor: el que manda es la ventana de contexto, **cuya cifra en Free no está publicada en ninguna parte** (el artículo que la explica se titula literalmente *"…on paid Claude plans"*). Un PDF de 1000 páginas no cabe ni en los 200K tokens de los planes de pago. Además, por encima de 100 páginas se apaga el análisis visual — y un escaneado sin capa de texto en ese tramo rinde prácticamente nada. | https://support.claude.com/en/articles/8241126-upload-files-to-claude · https://support.claude.com/en/articles/8606394-how-large-is-the-context-window-on-paid-claude-plans |
| **"El audio del dictado se borra: garantía relevante para el secreto profesional"** | **DUDOSO** (3/3 refutadores) | La cita es exacta pero la conclusión jurídica no se sigue. La garantía cubre **la grabación de audio**, no el texto transcrito ni el resto de la conversación, que siguen el régimen general de datos y alimentan la memoria entre conversaciones (encendida por defecto). Protege el archivo de sonido, no el contenido del caso. | https://support.claude.com/en/articles/10065434-use-dictation-on-claude-mobile |
| **"Compartir un chat no lleva los adjuntos"** | **DUDOSO como garantía de confidencialidad** | La cita es literal — *"the file itself is not included in the shared snapshot and remains private"* — y dos refutadores concluyen que la aparente contradicción con la página de artifacts se disuelve (son mecanismos distintos: compartir un CHAT vs publicar un ARTIFACT). El tercero se niega a darla por buena sin lectura directa por ser una garantía de confidencialidad. **Se aplica la lectura restrictiva: no prometérselo a una abogada hasta comprobarlo.** | https://support.claude.com/en/articles/10593882-share-and-unshare-chats |
| **"El cliente de Google Drive para escritorio es gratuito y no exige administrador"** | **DUDOSO — la fuente no dice lo que se le atribuye** | El **modo espejo** sí está confirmado: *"Mirrored files will always be stored on your computer and in the cloud. They are always available offline."* Pero la página citada **no afirma gratuidad, ni tipo de cuenta, ni ausencia de administrador**: tres extremos se apoyan en una fuente que no los contiene. Un refutador sí encontró evidencia lateral a favor (el propio Google dice que el problema de administrador aparece **con cuentas de trabajo o estudio**, no personales). Barrera dura de capacidad: **15 GB compartidos** entre Drive, Gmail y Fotos, y el espejo exige tanto espacio en disco local como ocupe el Drive. | https://support.google.com/drive/answer/13401938?hl=en · https://support.google.com/drive/answer/6374270 |
| **"OneDrive personal deja una copia real en el disco"** | **DUDOSO — matizado por una barrera técnica** | La cuenta personal sí es aceptada por el asistente, sin tenant de Entra ni administrador (esto **corrige** la conclusión anterior del proyecto: lo inalcanzable era el **conector** de Microsoft 365, no el contenido del OneDrive personal). Pero con **Files On-Demand, activo por defecto**, los archivos son marcadores en línea y **no ocupan disco** salvo que se marquen expresamente "Mantener siempre en este dispositivo". Sincronizar no significa tener los bytes. 5 GB gratuitos, compartidos con adjuntos de Outlook.com. | https://support.microsoft.com/en-us/office/sync-files-with-onedrive-in-windows-615391c4-2bd3-4aae-a42a-858262e42a49 · https://support.microsoft.com/en-us/onedrive/microsoft-storage-quotas |
| **Cowork existe en el plan Free** (afirmación que un artículo de conectores permite leer) | **REFUTADO** | El artículo de conectores enumera Cowork entre las superficies donde funciona el mecanismo, junto a los planes que pueden usarlo — no le concede Cowork al plan Free. **Los tres refutadores coinciden en que aquí no hay contradicción real**, y la restricción de la página específica de Cowork manda. | https://support.claude.com/en/articles/13345190-get-started-with-claude-cowork |

### 1.C — Exige pago, y cuánto

| Qué exige pagar | Plan mínimo | Precio literal | Fuente |
|---|---|---|---|
| **Cowork** (leer y escribir el expediente en disco, sub-agentes, hooks, terminal, proyectos locales con memoria) | **Pro** | **17 USD/mes con suscripción anual (200 USD cobrados por adelantado); 20 USD/mes si se factura mensualmente.** Más impuestos aplicables. | https://claude.com/pricing |
| **Claude Code** (agente de terminal) | Pro | Incluido en Pro. Comparte contador con el chat. | https://support.claude.com/en/articles/11145838-use-claude-code-with-your-pro-or-max-plan |
| **Plugins** (el envase natural del Legal OS: skills + conector MCP + sub-agentes + hooks en una instalación) | Cualquier plan de pago | Incluido. *"Plugin support in Cowork is available as a beta for all paid Claude users."* | https://claude.com/docs/plugins/overview |
| **Complemento Claude para Word** (citas por sección, control de cambios, edición preservando estilos) | Pro | Incluido en Pro como *"Claude for Microsoft 365"*. Para Word de **escritorio** en Windows exige además suscripción a Microsoft 365; **Word en la web no la exige**. | https://claude.com/docs/office-agents/word |
| **Research** (investigación agéntica multi-paso con citas) | Pro | Incluido. Requiere búsqueda web activada. | https://support.claude.com/en/articles/11088861-use-research-on-claude |
| **Búsqueda de chats pasados** | Pro | Incluido. En Free hay memoria automática pero **no** archivo consultable. | https://support.claude.com/en/articles/11817273-use-claude-s-chat-search-and-memory-to-build-on-previous-context |
| **RAG del conocimiento de proyecto** (capacidad ×10 al acercarse al límite de contexto) | Pro | Incluido. Es lo que hace grande a un proyecto. | https://support.claude.com/en/articles/9517075-what-are-projects |
| **Proyectos ilimitados** | Pro | Incluido. En Free, cinco. | https://claude.com/pricing |
| **Tareas programadas** (vigilancia de términos) | Cualquier plan de pago | Incluido, pero **consumen la cuota general** y corren en la nube. | https://support.claude.com/en/articles/13854387-schedule-recurring-tasks-in-claude-cowork |
| **Claude en Chrome** (portales judiciales, radicación) | Cualquier plan de pago | Incluido. Solo Chrome. Panel lateral como sesión de Cowork: Max y Team, *"rolling out"* a Pro. | https://support.claude.com/en/articles/12012173-get-started-with-claude-in-chrome |
| **Dispatch** y **computer use** | **Pro o Max únicamente** | Incluidos. **Excluyen Team y Enterprise**: si el despacho creciera a Team, los perdería. | https://claude.com/docs/cowork/guide/dispatch.md · https://support.claude.com/en/articles/14128542-let-claude-use-your-computer-in-cowork |
| **Créditos de uso** (seguir trabajando tras agotar el límite) | Pro, Max 5x, Max 20x | *"Usage credits are billed at standard API rates."* Gasto variable no acotado por la suscripción. **En Free esta válvula no existe: al agotar el límite, se para.** | https://support.claude.com/en/articles/12429409-manage-usage-credits-for-paid-claude-plans |
| **El escalón siguiente si Pro se queda corto** | Max 5x / Max 20x | **100 USD/mes** y **200 USD/mes**. *"The Max plan is currently available as a monthly subscription only"* — **no hay descuento anual**: 1.200 o 2.400 USD al año. | https://support.claude.com/en/articles/11049741-what-is-the-max-plan |
| **Team** (descartado) | — | *"Team plans require a minimum of two members."* **Una sola persona no puede contratarlo.** 25 USD/miembro/mes mensual, 20 USD anual. | https://support.claude.com/en/articles/9266767-what-is-the-team-plan |
| **Monitorización auditable de Cowork (OpenTelemetry)** | Team o Enterprise + administrador | Fuera de su alcance. Importa por lo que revela: **la única trazabilidad auditable de Cowork vive detrás de un plan de empresa.** Si el Legal OS necesita registro probatorio de lo que hizo la máquina, lo tenemos que construir nosotros. | https://claude.com/docs/cowork/monitoring |

**No existe prueba gratuita de Pro** [NOT FOUND], **no existe plan intermedio entre Free y Pro**, y **ninguno de los cuatro programas de acceso gratuito o con descuento localizados aplica a una profesional independiente del derecho** (educadores K-12 verificados, universidades, organizaciones sin ánimo de lucro con mínimo dos asientos, mantenedores de código abierto de alto impacto). Ver §8.

---

## §2 — Cowork a fondo

Todo lo que sigue **presupone un plan de pago**. Cuando una fila dice "sin costo adicional", significa *una vez pagado Pro* — y con una advertencia que vale para toda la sección: **"sin costo adicional" es falso en el único recurso que de verdad escasea.** *"Working on tasks with Cowork consumes more of your usage allocation than chatting with Claude."* Esa cuota es la misma del chat: cada tarea de Cowork le resta mensajes de conversación. (https://support.claude.com/en/articles/13345190-get-started-with-claude-cowork)

### 2.1 — Arquitectura: dónde corre realmente el trabajo

| Hecho | Etiqueta | Detalle y límite | Fuente |
|---|---|---|---|
| **Las sesiones corren en la nube por defecto** | VERIFICADO | *"the agent loop and code execution run on Anthropic's servers, and sessions and files are saved to the member's Claude account."* Cada sesión recibe un sandbox propio, destruido al terminar. En Team el interruptor "Run Cowork in the cloud" viene activado; en Enterprise desactivado. **Para Pro y Max no se documenta interruptor equivalente** → §9, pregunta 1. | https://support.claude.com/en/articles/14479288-claude-cowork-architecture-overview |
| **Sesión local: VM aislada por el hipervisor** | VERIFICADO | *"Shell commands and any code Claude writes execute inside a dedicated Linux VM, isolated from the host operating system by the platform's hypervisor (Apple Virtualization.framework on macOS, Hyper-V on Windows)."* No requiere WSL. Es la única configuración en la que el material no sale de su computador. | https://support.claude.com/en/articles/14479288-claude-cowork-architecture-overview |
| **El aislamiento NO limita lo que Claude lee** | VERIFICADO — advertencia del propio fabricante | *"Isolation limits where Claude's code runs. It doesn't limit what Claude reads or does."* **No se puede vender el sandbox como garantía de confidencialidad.** Lo que protege el material es la regla de carpetas conectadas. | https://support.claude.com/en/articles/13364135-use-claude-cowork-safely |
| **Los servidores MCP locales no corren en sesiones en la nube** | VERIFICADO — crítico para el diseño | *"Local MCP servers don't run in sessions in the cloud."* Como la nube es el modo por defecto, **nuestro Core MCP local no funcionaría salvo que ella pueda forzar sesión local.** | https://support.claude.com/en/articles/14479288-claude-cowork-architecture-overview |
| **Windows exige Virtual Machine Platform** | VERIFICADO — bloqueante potencial | *"Claude Desktop for Windows requires the Virtual Machine Platform to use Cowork."* Se activa con la característica opcional homónima de Windows, lo que exige permisos de administrador local. *"Virtual machines and VDI environments without nested virtualization aren't supported."* | https://support.claude.com/en/articles/12622703-deploy-claude-desktop-for-windows |
| **Conexión a internet permanente** | VERIFICADO | *"Active internet connection: Required throughout the session."* Almacenamiento local **no es** procesamiento local. | https://support.claude.com/en/articles/13345190-get-started-with-claude-cowork |
| **Disponibilidad por superficie** | VERIFICADO | Escritorio: todos los planes de pago, y es la única superficie con archivos locales, navegador y computer use — *"Desktop is the full Cowork experience"*. Web y móvil (beta): Pro, Max, Team; Enterprise si un administrador lo habilita. Chrome: Max y Team, *"and on Pro plans as it rolls out"*. **Web y móvil NO dan acceso a archivos locales** salvo con la app de escritorio abierta en ese computador. | https://support.claude.com/en/articles/15520349-use-claude-cowork-on-web-desktop-and-mobile |

### 2.2 — Acceso a archivos: la garantía real de compartimentación (resuelve B-04)

| Hecho | Etiqueta | Detalle y límite | Fuente |
|---|---|---|---|
| **El acceso se limita a las carpetas conectadas, y cada llamada se comprueba** | VERIFICADO | *"Local file access is limited to folders the member has connected on the desktop, and each local tool call is checked against the member's permissions before it runs."* **Es el mecanismo de compartimentación por expediente**: un caso por carpeta, y solo esa carpeta conectada. | https://support.claude.com/en/articles/14479288-claude-cowork-architecture-overview |
| **Es un control de capa de aplicación, no del sistema operativo** | VERIFICADO | *"Access is gated by an application-layer permission system."* Sirve para el diseño; **no es argumento de seguridad absoluta ante un cliente.** | https://support.claude.com/en/articles/14479288-claude-cowork-architecture-overview |
| **Dentro de una carpeta conectada, alcanza todo lo que alcance la cuenta del sistema** | VERIFICADO | *"Within an attached read/write folder, the agent can read and write every file the user's OS account can reach. To keep data out of reach entirely, leave it outside the allowed roots."* La granularidad es la **carpeta**, no el archivo. | https://claude.com/docs/third-party/claude-desktop/local-access |
| **NO hay reglas de denegación por ruta para un usuario individual** | NOT FOUND | La lista blanca de carpetas solo se documenta como configuración gestionada por MDM. Para un usuario sin administrador el comportamiento documentado es *"Unrestricted. Users can attach any folder they have OS-level access to."* **Su única herramienta de compartimentación es elegir bien qué carpeta conecta.** | https://claude.com/docs/third-party/claude-desktop/local-access |
| **Modo de solo lectura y carpeta de salidas de sesión** | VERIFICADO, **pero fuera de su alcance** | En modo `ro`, *"in Cowork, writes are blocked and Claude is directed to put modified copies in the session outputs folder."* Sería el patrón ideal para material probatorio (leer el original sin tocarlo, escribir aparte), pero **solo existe vía configuración gestionada por administrador**. | https://claude.com/docs/third-party/claude-desktop/local-access |
| **Unidades de red mapeadas en Windows** | VERIFICADO | Funcionan si están mapeadas a letra y accesibles **antes** de que arranque el sandbox. **Las rutas UNC crudas NO están soportadas.** Y: *"The agent cannot attach a network-drive path on its own; only the user can, through the folder picker. This is a security boundary."* | https://claude.com/docs/third-party/claude-desktop/local-access |
| **El borrado permanente SIEMPRE pide aprobación** | VERIFICADO | *"Claude always asks before permanently deleting files, in any mode."* Es el único freno duro documentado; todo lo demás depende del modo elegido. | https://support.claude.com/en/articles/13364135-use-claude-cowork-safely |
| **Tres modos de aprobación** | VERIFICADO | *Manual* (pide permiso por acción), *Auto* (sigue sin preguntar, revisando y bloqueando lo inseguro; **consume más cuota**), *Skip* (*"Claude doesn't pause to ask and nothing checks its actions automatically"*). **Para material de contraparte el modo debe ser Manual; Skip no debería ofrecerse nunca en un flujo probatorio.** | https://support.claude.com/en/articles/13345190-get-started-with-claude-cowork |
| **Lista cerrada de formatos que Cowork lee del disco** | NOT FOUND | No existe página oficial que la enumere. Sí consta: creación de .docx/.xlsx/.pptx/.pdf con tope de 30 MB, lectura de archivos individuales **hasta 50 MB** en proyectos, y que el changelog añadió soporte de .doc heredados y de .xls/.xlsx como texto adjunto. **Hay que probarlo con sus formatos reales, incluidos PDF escaneados.** | https://claude.com/docs/cowork/changelog |

### 2.3 — Proyectos de Cowork (distintos de los de claude.ai)

| Hecho | Etiqueta | Detalle y límite | Fuente |
|---|---|---|---|
| **Qué agrupa un proyecto** | VERIFICADO | Descripción (que Dispatch lee para elegir proyecto), carpetas locales de lectura/escritura, instrucciones permanentes, enlaces de referencia, proyectos de claude.ai vinculados, y **memoria propia que persiste entre sesiones**. | https://claude.com/docs/cowork/guide/projects |
| **Viven solo en el computador** | VERIFICADO (el hecho) — **DUDOSO como garantía de confidencialidad** | *"Projects live on your computer. They aren't synced to the cloud or shared with other people."* **Pero almacenamiento local no es procesamiento local**: la sesión corre en la nube por defecto y exige internet permanente. Dos refutadores advierten expresamente contra usar esta frase como argumento de secreto profesional. | https://claude.com/docs/cowork/guide/projects |
| **Memoria persistente y aislada por proyecto** | VERIFICADO | *"what Claude learns during the session is saved to the project's memory for next time."* Lo aprendido en un proyecto **no** se transfiere a otro. **Es exactamente la disciplina que exige el secreto profesional: un proyecto por expediente da compartimentación de contexto además de compartimentación de archivos.** Sin límite de tamaño documentado. | https://claude.com/docs/cowork/guide/projects |
| **Archivar borra la memoria, no los archivos** | VERIFICADO | *"Archiving… deletes its metadata (name, instructions, links, memory). It does not touch the local folders you attached."* Al cerrar un caso, el expediente en disco queda intacto **pero se pierde la memoria del caso**, que puede ser valiosa para recursos posteriores. Irreversible según la redacción. | https://claude.com/docs/cowork/guide/projects |
| **Lectura de archivos individuales hasta 50 MB** | VERIFICADO | *"Claude reads individual files up to 50 MB."* Límite **distinto** de los 30 MB de creación/subida. Un solo PDF escaneado de un expediente puede superarlo. | https://claude.com/docs/cowork/guide/projects |
| **Se puede enlazar un proyecto de claude.ai** | VERIFICADO | *"Linking doesn't merge them."* Permite tener doctrina y plantillas reutilizables en claude.ai y el material del caso en carpetas locales, sin mezclarlos. | https://claude.com/docs/cowork/guide/projects |
| **Número máximo de proyectos y de carpetas por proyecto** | NOT FOUND | No documentados. | https://claude.com/docs/cowork/guide/projects |
| **Las instrucciones de carpeta las puede actualizar Claude durante la sesión** | VERIFICADO (el hecho) — **riesgo abierto** | El usuario fija instrucciones a nivel de carpeta y Claude también puede actualizarlas durante las sesiones. **No se documenta si esa escritura pide aprobación** → §9, pregunta 6. Vector de inyección persistente: un documento de contraparte con instrucciones ocultas podría intentar alterar la conducta futura del sistema sobre ese expediente. | https://support.claude.com/en/articles/13345190-get-started-with-claude-cowork |

### 2.4 — Delegación: Dispatch, tareas programadas, computer use

| Capacidad | Plan | Detalle y límite | Fuente |
|---|---|---|---|
| **Dispatch** — agente de larga duración que parte un encargo en tareas hijas | **Pro o Max ÚNICAMENTE** (excluye Team y Enterprise) | *"You converse with one Dispatch agent, but it can run many child tasks… Child tasks don't spawn further children."* **Un solo hilo**: *"There's no way to start a new thread or manage multiple threads"* — obliga a diseño cuidadoso con varios casos vivos. Exige el computador despierto y la app abierta. | https://claude.com/docs/cowork/guide/dispatch |
| **Dispatch deniega solo a los diez minutos** | VERIFICADO — **modo de fallo silencioso** | *"If you don't respond within ten minutes, the request is automatically denied and the task continues without that action."* La tarea **no se detiene ni avisa**: entrega un resultado mutilado que parece completo. En trabajo jurídico desatendido esto exige verificación de completitud diseñada aparte. | https://claude.com/docs/cowork/guide/dispatch |
| **Dispatch desde el móvil, ejecutando en el escritorio** | Pro o Max | *"Your desktop must be awake and the Claude Desktop app open while Claude works."* Encargar desde audiencia un trabajo que corre sobre los expedientes de su computador. Si el equipo se apaga, la tarea muere. | https://support.claude.com/en/articles/13947068-assign-tasks-from-anywhere-in-claude-cowork |
| **Tareas programadas** | Todos los planes de pago | Cadencias: por hora, diaria, semanal, días hábiles, o manual. Cada tarea corre como su propia sesión. **Corren en la nube**: *"Scheduled tasks run remotely, so they run on their cadence even when your computer is asleep or the Claude Desktop app is closed."* **Consumen la cuota general** (el changelog eliminó el cupo diario separado). Número máximo de tareas: NOT FOUND. | https://support.claude.com/en/articles/13854387-schedule-recurring-tasks-in-claude-cowork |
| **¿Vigilan un expediente en disco?** | **INCONCLUSIVE — contradicción interna en la misma página** | *"They can't be tied to a folder on your computer"* junto a *"If a scheduled task requires local files or apps, it will only run locally."* **No se puede prometer vigilancia programada sobre su expediente en disco** → §7.5. Riesgo añadido: una tarea que se dispara sola consume cuota sin que ella lo decida, y puede agotar la ventana de 5 horas de madrugada. | https://support.claude.com/en/articles/13854387-schedule-recurring-tasks-in-claude-cowork |
| **Computer use** — Claude opera la pantalla | **Pro y Max ÚNICAMENTE**, research preview | *"Claude asks for your permission before accessing each application."* Es la única vía para software jurídico de escritorio sin API ni conector. macOS y Windows; no en la beta de Linux. Algunas aplicaciones sensibles bloqueadas por defecto. **"Research preview" significa que el proveedor se reserva cambiarla o retirarla: no se debe construir un flujo con término procesal sobre ella.** | https://support.claude.com/en/articles/14128542-let-claude-use-your-computer-in-cowork |
| **Claude en Chrome** | Todos los planes de pago | *"Claude to read, click, and navigate websites alongside you"*, incluido rellenar formularios. **Solo Chrome**: *"not supported on other Chromium-based web browsers or mobile devices"* — ella tendría que instalarlo y migrar su trabajo. La extensión pide 16 permisos, incluido acceso al depurador, y se autoriza **sitio por sitio**. Alto valor práctico en Colombia (Rama Judicial, radicación, SAMAI); alto riesgo: el propio fabricante lo llama arriesgado y **los permisos de egress de red no se le aplican**. | https://support.claude.com/en/articles/12012173-get-started-with-claude-in-chrome |

### 2.5 — Extensibilidad: plugins, skills, sub-agentes, hooks

| Hecho | Etiqueta | Detalle y límite | Fuente |
|---|---|---|---|
| **Hooks y sub-agentes corren ÚNICAMENTE en Cowork** | VERIFICADO — **decisivo para el producto** | *"Hooks and sub-agents run only in Cowork, so they appear grayed out in chat."* Si el Legal OS necesita ejecutar lógica propia (validaciones, registro de artefactos, controles de trazabilidad), **Cowork es la única superficie posible**, y eso ata el producto a un plan de pago. | https://support.claude.com/en/articles/13837440-use-plugins-in-claude |
| **Un plugin empaqueta todo en una instalación** | VERIFICADO | Skills, conectores MCP, sub-agentes, comandos slash y hooks *"in a single step"*. Tras instalar se pueden habilitar componentes individuales. Es el envase natural del Legal OS. En beta; guardados localmente. | https://claude.com/docs/cowork/guide/plugins |
| **Un repositorio git propio sirve de marketplace privado** | VERIFICADO (3/3 refutadores) — **mejor vía de distribución del inventario** | *"A Git repository that contains plugin packages can serve as a marketplace. This is the typical way teams distribute their own plugins without publishing to the public catalog."* Se acepta la URL completa de GitHub y el atajo propietario/repositorio; botón **Update** para traer la última versión. Sin administrador, sin revisión de Anthropic, sin catálogo público. **Barrera:** la privacidad solo existe en GitHub — *"public repositories on GitLab and Bitbucket also work"*, es decir en esas dos el repositorio **debe ser público**. **Abarata la ENTREGA, no el CONSUMO.** | https://claude.com/docs/cowork/guide/plugins |
| **Un plugin puede traer un servidor MCP local** | VERIFICADO en Claude Code — **POR VERIFICAR en Cowork** | *"Plugins can contain any MCP, including remote MCPs, local MCPs, and MCPBs."* **Contradicción abierta** (§7.13): la única especificación del archivo de configuración localizada es la de plugins de organización en despliegue de terceros, y **solo admite `http` y `sse`, ningún proceso local stdio**. Hay que probarlo empíricamente antes de comprometerlo en el diseño. | https://claude.com/docs/plugins/submit · https://claude.com/docs/third-party/claude-desktop/extensions |
| **SETUP.md: el plugin guía su propia configuración** | VERIFICADO (existencia) — formato NOT FOUND | *"Plugins can include a SETUP.md skill to guide Claude through configuring and connecting any MCP servers bundled in the plugin."* Convertiría la instalación del Core en algo que Claude conduce paso a paso. **No se documenta el formato ni la ubicación del archivo.** | https://claude.com/docs/plugins/submit |
| **Cowork NO lee el directorio de Claude Code en su máquina** | VERIFICADO | *"Cowork loads the ones enabled for your claude.ai account, synced at session start, and doesn't read the Claude Code CLI's ~/.claude directory."* Lo que construyamos para Claude Code **no llega solo** a su Cowork. Y la sincronización es al **inicio de sesión**: tras actualizar el plugin, ella debe reiniciar la sesión. | https://claude.com/docs/cowork/overview |
| **Sub-agentes: sin control de usuario documentado** | INCONCLUSIVE | *"Complex work gets divided into smaller tasks with parallel workstreams."* Pero **no existe en Cowork ninguna interfaz documentada para crear, editar, limitar o asignar permisos a sub-agentes**, ni cuántos corren en paralelo. Lo que existe documentado en ese sentido pertenece a Claude Code. **No prometer "un sub-agente revisor y otro redactor" sin probarlo.** | https://claude.com/docs/cowork/overview |
| **Límites del paquete** | VERIFICADO | Paquete sin comprimir: **200 MB**. Archivos por paquete: **5.000**. Archivo del repositorio de marketplace: **512 MB**. Plugins por marketplace: **500**. Marketplaces añadibles: **25**. El visor previsualiza archivos de hasta 1 MB; los mayores siguen disponibles en ejecución. Holgado para nuestro producto. (Ojo: el artículo de administración de organización da cifras distintas — §7.14.) | https://claude.com/docs/cowork/guide/plugins |
| **Existe un plugin oficial "Legal"** | VERIFICADO — **utilidad parcial, hay que ser honestos** | *"Review documents, flag risks, and track compliance"* / *"…for in-house legal teams"*. Un refutador lo abrió: **no trae ningún conector** — aporta cinco comandos y remite a que el usuario ponga sus propios MCP: *"Connect your document management, chat, and project tracking tools via MCP for richer context."* **Está escrito para abogacía in-house de empresa, no para litigio colombiano.** Sirve como referencia de arquitectura, no como sustituto de lo que hay que construir. | https://claude.com/docs/plugins/overview |
| **Existe un plugin "Cowork Plugin Management"** | VERIFICADO | *"MCP server creation and customization"*. Ninguna utilidad directa para ella; **muy relevante para nosotros** como vía corta para construir y empaquetar el MCP local del Core. Detalle funcional no verificado. | https://claude.com/plugins-for/cowork |
| **Publicar en el directorio oficial exige repositorio PÚBLICO** | VERIFICADO | *"The repo must be public—closed-source plugins are not accepted."* Y por la vía claude.ai exige organización Team o Enterprise. **No nos hace falta y conviene evitarlo**: el marketplace propio en GitHub logra la distribución sin publicar nada. | https://claude.com/docs/plugins/submit |

### 2.6 — Lo que el changelog revela y el equipo no conocía

Todo lo de esta subsección procede de https://claude.com/docs/cowork/changelog salvo indicación contraria. Es la fuente menos leída y la que más cambia el diseño.

| Hallazgo | Por qué importa |
|---|---|
| **Ventana de contexto de 1M en tareas de Cowork, con controles de esfuerzo y de razonamiento dentro de la sesión** — *"Added in-session effort and thinking controls for local Cowork projects."* | **Es lo que hace viable analizar un expediente completo de una sola vez** en lugar de por trozos. Prácticamente nadie lo conoce. Aviso: un fallo corregido indica que las tareas programadas corrían en el modelo de 200K cuando se había elegido la fila de 1M; el formulario ahora la etiqueta. |
| **Comandos `/usage` y `/cost` dentro de las tareas** — *"an inline card shows your plan limits and the session's usage without sending anything to the model."* | Puede ver cuánto le está costando un encargo **sin gastar cuota para averiguarlo**. Herramienta concreta de control de gasto en sesiones largas sobre un expediente. |
| **Reanudación automática al reiniciarse el límite de 5 horas, activada por defecto** — *"sessions left open resume when the limit resets."* | Mitiga el corte de cinco horas en tareas largas, **pero también significa que puede consumir cuota sin supervisión.** Se desactiva desmarcando "Auto-continue when limits reset" en el banner. Debe conocerlo antes de dejar una tarea corriendo. |
| **Editor de documentos con conteo de palabras en vivo** — *"Added a live word count and a copy button to each document bar above the composer"*; y los Markdown que Claude entrega *"open in the document editor instead of a plain-text preview."* | Directamente aplicable a **memoriales con límite de extensión**. Redactar y revisar dentro de la misma herramienta. |
| **Soporte de Office heredado** — *"Added support for legacy Word .doc files, which now open like .docx, and Excel .xlsx and .xls spreadsheets, which now attach as text where they used to be refused."* | **Corrige un hallazgo previo del proyecto.** Muchos juzgados y contrapartes en Colombia siguen enviando .doc. Sigue sin estar soportado en el complemento de Word. Verificar la versión instalada antes de prometerlo. |
| **Vista unificada de Artifacts y home unificado de Chat y Cowork** — *"lists your chat, Code, and Cowork artifacts in one searchable place."* | Los entregables de todos los casos quedan localizables en un sitio. **También es un riesgo de mezcla visual entre asuntos si no se nombran con disciplina.** |
| **Gestión de disco** — *"Added a 'Free Up Cowork Disk Space' option under Help > Troubleshooting"*, con limpieza automática de cachés cuando el disco del espacio de trabajo se queda corto. | Cowork ocupa disco de forma no trivial. Con expedientes escaneados grandes hay que contar con espacio libre y saber dónde está el botón. |
| **Terminal real dentro de la VM**, con el fallo corregido de ofrecerla en dispositivos sin virtualización (ChromeOS), *"where every command immediately failed"*. | Es lo que permite **procesar lotes**: convertir, renombrar, extraer, contar e indexar cientos de archivos de un expediente sin subirlos a ningún sitio. |
| **Las rutinas pasaron a consumir el límite general** — *"Changed routines to count against your regular usage limits instead of a separate daily included-run limit."* | Automatizar ya no es gratis en cuota: **cada ejecución programada le resta trabajo manual.** |
| **Existe un "weekly Cowork limit"** — *"Fixed chat refusing new messages after the weekly Cowork limit was used up."* | Revela dos cosas: que existe un tope semanal asociado a Cowork, y que **agotarlo llegó a bloquear el chat normal**. Contradice al centro de ayuda (§7.8). La cifra no está publicada en ninguna parte. |
| **Live artifacts** (https://support.claude.com/en/articles/14729249-use-live-artifacts-in-claude-cowork) — paneles HTML persistentes que al abrirse *"can pull from your connected apps and local files so the view reflects today"*. | Un tablero de cartera de casos que se actualiza solo es de altísimo valor. **Pero:** *"artifacts don't ask for permission before using connectors, even if your session mode would normally require approval."* Salta el modelo de permisos. **Regla de diseño obligada: un artifact por proyecto, nunca uno transversal.** Solo escritorio; no viajan entre dispositivos; en Pro y Max no se pueden compartir ni publicar. |

---

## §3 — El resto del arsenal

Capacidades transversales, que no dependen de Cowork. Aquí es donde vive la ruta sin costo, y también donde están las trampas.

### 3.1 — Trabajo con documentos y datos

| Capacidad | Plan | Etiqueta | Detalle y límite | Fuente |
|---|---|---|---|---|
| **Ejecución de código y creación de archivos** | Free en adelante | VERIFICADO | *"Code execution and file creation is available to all Claude users (Free, Pro, Max, Team, and Enterprise) on the web, Claude Desktop, and Claude Mobile."* Produce .docx, .xlsx **con fórmulas funcionales**, .pptx y .pdf. Entorno aislado en contenedor. 30 MB por archivo, subida y descarga. **Desactivar el acceso de red del sandbox es opción solo de Team/Enterprise.** | https://support.claude.com/en/articles/12111783-create-and-edit-files-with-claude |
| **Aritmética ejecutada en vez de estimada** | Free | VERIFICADO (derivado de la anterior) | Liquidaciones, intereses, términos y tablas de vencimientos calculados con código, no con prosa. **Para trabajo jurídico esto vale más que la redacción: elimina el error de cálculo mental del modelo.** | https://support.claude.com/en/articles/12111783-create-and-edit-files-with-claude |
| **¿Editar un .docx o .xlsx ya subido y devolverlo modificado?** | — | **INCONCLUSIVE** | El artículo se titula "Create and edit files" pero el cuerpo consultado **solo documenta creación**. La vía VERIFICADA para "tome este contrato y devuélvamelo con los cambios" es el **complemento de Word con control de cambios (Pro+)**, no la conversación. **No prometer edición en el sitio hasta comprobarlo.** | https://support.claude.com/en/articles/12111783-create-and-edit-files-with-claude |
| **Subida de archivos: tipos admitidos** | El artículo no diferencia por plan | VERIFICADO (los tipos) | Documentos: PDF, DOCX, CSV, TXT, HTML, ODT, RTF, EPUB, JSON, XLSX. Imágenes: JPEG, PNG, GIF, WebP. **No figura ningún formato de audio ni de vídeo.** XLSX exige tener activada la ejecución de código. | https://support.claude.com/en/articles/8241126-upload-files-to-claude |
| **Cuántos archivos y de qué tamaño** | — | **DUDOSO / REFUTADO como promesa** (§1.B) | Chat: *"Up to 20 files per chat"*, *"500MB per file"*. **Proyectos: 30 MB por archivo.** Creación/descarga: 30 MB. Cowork: 50 MB por archivo. **Cuatro cifras en cuatro superficies** (§7.9). Y ninguna describe capacidad de trabajo: el techo real es la ventana de contexto, y la de Free no está publicada. | https://support.claude.com/en/articles/8241126-upload-files-to-claude |
| **Análisis de PDF** | El artículo no diferencia por plan | **DUDOSO** | *"Claude analyzes both text and visual elements… in PDFs of 100 pages or fewer. For PDFs from 101 to 1000 pages, Claude processes text only and doesn't analyze visual elements."* Máximo 1000 páginas. **Consecuencia crítica, marcada como riesgo y no como hecho: un PDF escaneado de más de 100 páginas cae en el tramo "solo texto", y un escaneado no tiene texto.** Hay que partirlo en bloques de 100 páginas o menos. | https://support.claude.com/en/articles/8241126-upload-files-to-claude |
| **Lectura de escaneados (el pipeline real)** | Documentado para la API, **no para claude.ai** | VERIFICADO con reserva de superficie | *"The system converts each page of the document into an image. The text from each page is extracted and provided alongside each page's image."* **Funcionalmente lee material escaneado por visión; la documentación nunca usa la palabra OCR**, y no existe ninguna página que prometa OCR en claude.ai. Consejo oficial para escaneados: *"Rotate pages to proper upright orientation."* | https://platform.claude.com/docs/en/build-with-claude/pdf-support |
| **Citar el folio exacto de un escaneado** | — | **NOT FOUND / negado** | *"As image citations are not yet supported, PDFs that are scans of documents and do not contain extractable text are not citable."* Además, para .docx y .xlsx **no hay soporte de citas**: hay que convertirlos a texto plano. **No prometer trazabilidad a folio como función de plataforma.** | https://platform.claude.com/docs/en/build-with-claude/citations |
| **Análisis de imágenes** | El artículo no restringe por plan | VERIFICADO con advertencia | Máximo 20 imágenes por mensaje, 10 MB por imagen, 8000×8000 px. **Advertencia literal: *"Claude might hallucinate or make mistakes when interpreting low-quality, rotated, or very small images under 200 pixels."*** Ese es exactamente el perfil del material judicial escaneado en Colombia. **Todo dato extraído de imagen exige revisión humana antes de convertirse en hecho del expediente.** No puede generar ni editar imágenes. | https://platform.claude.com/docs/en/build-with-claude/vision |

### 3.2 — Organización, memoria y continuidad

| Capacidad | Plan | Etiqueta | Detalle y límite | Fuente |
|---|---|---|---|---|
| **Proyectos de claude.ai** | Free (5) / Pro (ilimitados) | VERIFICADO (el número) | *"Free users can create a maximum of five projects."* **Precisión que dos refutadores exigieron:** *"Context is not shared across chats within a project unless the information is added into the project knowledge base"* — lo conversado en un chat **no** pasa solo al siguiente; hay que subirlo a la base de conocimiento. | https://support.claude.com/en/articles/9519177-how-can-i-create-and-manage-projects |
| **RAG del conocimiento de proyecto** | **Pro en adelante** | VERIFICADO — **barrera no prevista** | *"When your project knowledge approaches context limits, Claude seamlessly enables RAG mode to expand capacity by up to 10x"*, y esa mejora *"is only available to users with paid Claude plans"*. **En Free todo el conocimiento del proyecto debe caber crudo en la ventana de contexto, y la degradación es silenciosa: no hay aviso previo.** | https://support.claude.com/en/articles/9517075-what-are-projects |
| **Memoria entre conversaciones** | Free, Pro, Max: **activada por defecto** | VERIFICADO | *"Each project has its own separate memory space and dedicated project summary."* Controles: *Pause memory* y *Reset memory* (*"Permanently deletes all memories including project memories"*). En Team y Enterprise viene apagada. **Doble lectura: el aislamiento por proyecto es la propiedad que necesita el secreto profesional; que venga encendida por defecto es una decisión de privacidad tomada por omisión sobre datos de clientes.** | https://support.claude.com/en/articles/11817273-use-claude-s-chat-search-and-memory-to-build-on-previous-context |
| **Búsqueda de chats pasados** | **Pro en adelante** | VERIFICADO — barrera no prevista | *"Searching past chats is available to users on paid plans."* **En Free hay memoria automática pero el historial no es consultable a propósito.** Para un despacho que acumula expedientes es una fricción real. | https://support.claude.com/en/articles/11817273-use-claude-s-chat-search-and-memory-to-build-on-previous-context |
| **Importar, ver y editar la memoria** | Free, Pro, Max, Team (**Enterprise excluido**) | VERIFICADO, experimental | Se puede auditar qué sabe Claude de sus casos y borrar lo que no deba estar. *"Memory imports are experimental… Claude may not always successfully incorporate imported memories."* | https://support.claude.com/en/articles/12123587-import-and-export-your-memory-from-claude |
| **Exportar los datos propios** | Free, Pro, Max | VERIFICADO | Salvaguarda de continuidad frente a la dependencia del proveedor. No se puede lanzar desde iOS ni Android. **El enlace de descarga llega por correo y expira a las 24 horas.** | https://support.claude.com/en/articles/9450526-export-your-claude-data |
| **Gestión automática del contexto** (resumir conversaciones largas para que no se corten) | Ligada al interruptor de ejecución de código | VERIFICADO — **dependencia oculta** | *"Code execution must be enabled for automatic context management."* Y tiene precio: *"Longer conversations that trigger automatic context management consume more of your usage limit."* **Doble aviso para trabajo probatorio: la conversación larga sobre un caso no se corta, pero se resume — con pérdida potencial de detalle fáctico — y además cuesta más cuota.** | https://support.claude.com/en/articles/11647753-how-do-usage-and-length-limits-work |

> **El interruptor de ejecución de código es el punto único de fallo del plan gratuito.** De él cuelgan, todos a la vez: la creación de archivos, los Artifacts, las Skills, **la subida de XLSX** y **la gestión automática de contexto**. Viene APAGADO por defecto en planes personales (Settings > Capabilities). Una usuaria sin habilidades técnicas puede concluir que el producto no funciona cuando lo único que falta es ese interruptor. **Debe ser el paso 1 de cualquier guía de puesta en marcha.**

### 3.3 — Entrada de voz, búsqueda e investigación

| Capacidad | Plan | Etiqueta | Detalle y límite | Fuente |
|---|---|---|---|---|
| **Dictado** (habla → texto en el cuadro de mensaje) | Todos los planes | VERIFICADO — **solo móvil** | *"Dictation is available to all Claude users."* Español entre los doce idiomas listados; soporte no inglés marcado beta. **Barrera que cambia el diseño: *"when using Claude for iOS or Android"* — no existe en escritorio ni web.** El changelog registra dictado en el compositor de escritorio y en el panel de Chrome; **si eso ya está desplegado en su versión hay que comprobarlo** → §9. Solo habla en vivo: **no convierte una entrevista ya grabada.** | https://support.claude.com/en/articles/10065434-use-dictation-on-claude-mobile |
| **Garantía de borrado del audio** | — | **DUDOSO como argumento de secreto profesional** (3/3 refutadores) | *"After converting your speech input to text, we will delete your audio recording. We will not retain a copy… or use it for training."* **La garantía cubre la grabación, no el texto transcrito ni el resto de la conversación**, que siguen el régimen general de datos y alimentan la memoria. Protege el archivo de sonido, no el contenido del caso. | https://support.claude.com/en/articles/10065434-use-dictation-on-claude-mobile |
| **Modo voz** (conversación hablada) | Todos los planes, beta | VERIFICADO | Móvil, escritorio y web, *"built to work best from your phone"*. *"Voice conversations count toward your regular usage limits."* **El artículo no publica lista de idiomas para voz** y declara el soporte no inglés en beta. Es conversación con Claude, **no captura de un tercero**. | https://support.claude.com/en/articles/11101966-use-voice-mode |
| **Dictado dentro de los complementos de Office** | Hereda el plan de los complementos (Pro+) | VERIFICADO | **No funciona en Office en la web**: *"browser-hosted add-ins cannot access the microphone."* Exige autenticación directa con Claude. **Dato que hay que registrar en la cadena de tratamiento: *"Nothing is transcribed on your device. Audio is streamed to Anthropic, which uses a contracted speech-to-text subprocessor."*** El audio no se retiene tras transcribir. | https://claude.com/docs/office-agents/dictation |
| **Búsqueda web** | **DUDOSO en Free** | DUDOSO (los refutadores discrepan) | *"Every response includes citations, so you can easily verify sources yourself."* Consumo confirmado: *"Usage of web search and web fetch counts toward your daily limits."* **El artículo no declara ninguna matriz de planes**; el único apoyo para Free es la viñeta comercial de precios. Se activa manualmente por chat. Puede inferir su ubicación por IP. **Advertencia de veracidad: buscar en la web NO convierte lo hallado en derecho aplicable verificado.** | https://support.claude.com/en/articles/10684626-enable-and-use-web-search |
| **Research** (investigación agéntica multi-paso) | **Pro en adelante. Free excluido** | VERIFICADO | *"Research is available for users with paid Claude plans."* Exige búsqueda web activada. *"Research sessions can use up your limits faster due to Claude retrieving multiple sources."* **En la ruta sin costo hay que sustituirlo por búsqueda web manual, más lenta.** | https://support.claude.com/en/articles/11088861-use-research-on-claude |
| **Pensamiento extendido y nivel de esfuerzo** | **NO DECLARADO** | **INCONCLUSIVE** | Ninguna de las dos páginas consultadas declara qué planes lo incluyen (la viñeta *"Extended thinking for complex work"* figura en Free en precios, pero el artículo de la función no lo confirma). *"Higher effort means more thorough responses, but they take longer and use more tokens."* Y: *"Extended thinking cannot be turned off in Claude when using Claude Opus 5"* → mayor consumo por respuesta, que en un plan con cupo limitado es un costo real. | https://support.claude.com/en/articles/8664678-change-the-model-effort-and-thinking-settings |
| **Acceso a modelos por plan** | — | **INCONCLUSIVE** | La lectura de la tabla de precios es indirecta y choca con la viñeta de Pro *"Ability to use more Claude models"*. **No debe prometerse acceso a un modelo concreto en Free hasta comprobarlo en la propia cuenta.** | https://claude.com/pricing |

### 3.4 — Entregables, comparticiones y sus riesgos

| Capacidad | Plan | Etiqueta | Detalle y límite | Fuente |
|---|---|---|---|---|
| **Artifacts** | Free en adelante | VERIFICADO | Markdown y texto, código, HTML de una página, SVG, diagramas y componentes React. **Edición en el sitio para Markdown**: seleccionar texto, "Edit with Claude" y pedir el cambio ahí mismo — especialmente bueno para revisar una cláusula sin describir dónde está. Se crean con contenido *"significant and self-contained, typically over 15 lines"*. 20 MB por artifact. Prerrequisito duro: *"We no longer support artifacts without Code execution and file creation enabled."* Consumen cuota. | https://support.claude.com/en/articles/9487310-what-are-artifacts-and-how-do-i-use-them |
| **Publicar un artifact** | Free, Pro, Max | **VERIFICADO como riesgo** | *"Makes your artifact publicly available. Anyone with the link can view and interact with it"* y *"Non-users: View and interact… without signing up."* El remedio es destructivo: *"Once you unpublish an artifact, you cannot publish that same artifact again"* y *"Unpublishing also permanently deletes all associated storage data."* **Team y Enterprise no pueden publicar hacia afuera: la única protección corporativa es la que ella no tendrá.** Un refutador advierte además que compartir un artifact daría acceso a *"any attachments and files in the conversation that created it"*; los otros dos acotan esa frase al ámbito de organización. **Se aplica la lectura restrictiva: asumir que los adjuntos son alcanzables. Regla: no publicar nunca material de un caso.** | https://support.claude.com/en/articles/9547008-publish-and-share-artifacts |
| **Compartir una conversación** | Free en adelante | **DUDOSO como garantía** | *"If you share a chat that contains an attached file, the file itself is not included in the shared snapshot and remains private."* Se comparte una **instantánea**; los mensajes posteriores siguen privados; se revoca pasando de "Public" a "Private". Los datos crudos de llamadas MCP quedan ocultos. **Dos refutadores dan por disuelta la aparente contradicción con la página de artifacts; el tercero se niega a avalar una garantía de confidencialidad sin lectura directa. Hasta comprobarlo, tratar todo enlace compartido como potencialmente expositor.** | https://support.claude.com/en/articles/10593882-share-and-unshare-chats |
| **Idiomas** | No declarado por plan | VERIFICADO | Interfaz en *"Spanish (Latin America)"* y *"Spanish (Spain)"*, en web y escritorio. *"Claude will converse with you in the language you use."* **No existe función de traducción dedicada con garantías de fidelidad**: es capacidad conversacional. **Para prueba trasladada a un proceso, eso no basta y hay que decirlo.** | https://support.claude.com/en/articles/10769299-how-to-use-claude-in-your-preferred-language |

### 3.5 — Conectores y extensibilidad transversal

| Capacidad | Plan | Etiqueta | Detalle y límite | Fuente |
|---|---|---|---|---|
| **Conector personalizado por MCP remoto** | **Free (uno), Pro+ (sin cifra publicada)** | VERIFICADO | *"Free users are limited to one custom connector."* Sin administrador en Free y Pro; en Team/Enterprise *"only Owners can add them"*. **Es la única extensibilidad propia verificada sin pagar Claude.** | https://support.claude.com/en/articles/11175166-get-started-with-custom-connectors-using-remote-mcp |
| **Un MCP remoto NO puede alcanzar su disco** (resuelve V-5) | — | VERIFICADO — cierra una fantasía del diseño | *"Custom connectors (remote MCP servers) are reached from Anthropic's cloud infrastructure, not from your local machine. This is true even if you're using Cowork or Claude Desktop."* Y: *"Your server must be reachable over the public internet from Anthropic's IP ranges."* **Si el Core tiene que ver el disco, tiene que correr en el disco.** Costo oculto: alojamiento 24/7 — un hosting gratuito con suspensión por inactividad fallaría justo al empezar la jornada. La autenticación por cabeceras está en beta restringida. | https://support.claude.com/en/articles/11176164-use-connectors-to-extend-claude-s-capabilities |
| **Conectores prefabricados (Google, Microsoft, Slack)** | **REFUTADO en Free** | REFUTADO | Ver §1.B y §5. Ninguno es activable por ella sola y gratis: Google Drive/Gmail/Calendar restringidos a Pro+ por tres páginas de docs y por la línea de prerrequisitos del tutorial; **Microsoft 365 exige tenant de Entra, Global Administrator y rechaza cuentas personales**; **Slack exige aprobación de un administrador del espacio de trabajo**. | https://claude.com/docs/connectors/getting-started.md |
| **Directorio de conectores** | Catálogo vivo dentro del producto | **NOT FOUND** (su contenido y planes) | La documentación no publica la lista ni la disponibilidad por plan. **Advertencia que debe ser regla de gobierno del Legal OS:** *"Verified connectors have been tested by Anthropic for quality and compatibility… though verification is not a security audit"*, y *"once connected, a community connector has the same capabilities and access as any connector you grant."* **Ningún conector comunitario tocando expedientes sin decisión explícita y documentada.** | https://claude.com/docs/connectors/directory |
| **MCP Apps** (interfaz visual dentro de la conversación) | **NO DECLARADO** | VERIFICADO (existencia), plan NOT FOUND | Servidores MCP que además de herramientas aportan interfaz, renderizada en línea en la conversación. Se configuran en `Settings > Developer` con "Edit Config". **Doble valor:** podría dar al Legal OS una ficha de caso o una tabla de hechos reales dentro del chat, en lugar de solo texto; y es **un cuarto dato en la contradicción de MCP local** (§7.2), porque describe configurar servidores MCP locales en Claude Desktop sin restringir plan. | https://claude.com/docs/connectors/building/mcp-apps/getting-started |
| **Registro de conectores instalados en este entorno** | — | NOT FOUND | La consulta al registro con las palabras clave google, drive, gmail, calendar, onedrive, microsoft, dropbox, box y notion devolvió vacío. **Marca el límite de esta verificación: lo que ella tenga realmente disponible solo se sabe abriendo su cuenta, en Customize > Connectors.** | https://claude.com/docs/connectors/directory |
| **Los permisos de egress de red no cubren las cuatro vías más probables de salida** | Control de organización | VERIFICADO | *"Network egress permissions don't apply to the web fetch or web search tools or MCPs, including Claude in Chrome."* **No se puede prometer contención de red apoyándose en el egress.** | https://support.claude.com/en/articles/13364135-use-claude-cowork-safely |
| **Inyección de instrucciones: riesgo declarado, mitigación parcial** | — | VERIFICADO | *"Web content is a primary vector for prompt injection attacks—malicious instructions can be hidden in websites, emails, or documents Claude reads."* Los clasificadores **señalan** posibles inyecciones; **no se declara que las bloqueen con garantía**. **Leer documentos de la contraparte ES su trabajo. Obliga a modo Manual y revisión humana en todo flujo con material adverso.** | https://support.claude.com/en/articles/13364135-use-claude-cowork-safely |

---

## §4 — Skills y plugins: cómo se distribuye e instala nuestro producto

### 4.1 — La pregunta abierta que decide si el primer entregable es gratuito

**¿Las Skills funcionan en el plan gratuito? — DUDOSO. Los refutadores discrepan y no hay árbitro documental.**

- La documentación técnica **excluye Free**: *"Skills are available for users on Pro, Max, Team, and Enterprise plans. The Skills feature requires code execution to be enabled."* — https://claude.com/docs/skills/overview
- **Tres artículos de soporte** dicen lo contrario con la misma frase salvo una palabra: *"Skills are available for users on **Free**, Pro, Max, Team, and Enterprise plans."* — https://support.claude.com/en/articles/12512180-use-skills-in-claude · https://support.claude.com/en/articles/12512176-what-are-skills · https://support.claude.com/en/articles/12512198-how-to-create-custom-skills
- **Se buscó desempate en la página comercial y no existe: "Skills" no aparece en ninguna viñeta, ni de Free ni de Pro.** — https://claude.com/pricing

Dos refutadores la dejan DUDOSA y aplican el sesgo restrictivo. **El tercero la da por resuelta a favor de Free** y sostiene que el error fue trasladar a las Skills la restricción de Cowork y de los plugins, que son productos distintos. **Se aplica la regla: gana la lectura más restrictiva, y se deja constancia de que discrepan.** No se puede prometer que `fact-builder` funcione sin costo hasta probarlo.

**Barrera que sobrevive aunque se resuelva a favor de Free:** una skill en el plan gratuito sería **una plantilla de instrucciones, no lógica ejecutable**. No podría empaquetarse como plugin (de pago) ni usar hooks ni sub-agentes (solo Cowork, de pago). El premio es mucho menor de lo que parece.

**Indicio para diseñar la prueba empírica** (es indicio, no verificación): la creación de archivos y las Skills comparten el mismo prerrequisito — el interruptor de ejecución de código — y ese interruptor **sí está disponible en Free**. Si en su cuenta gratuita aparece el menú **Customize > Skills** con el botón de subir, la contradicción se resuelve en un minuto y sin gastar nada.

### 4.2 — Cómo se escribe un skill

| Hecho | Etiqueta | Detalle | Fuente |
|---|---|---|---|
| **Formato: texto plano, estándar abierto** | VERIFICADO (3/3) — **no depende de ningún plan** | Un directorio con `SKILL.md` obligatorio y, opcionalmente, `scripts/` (código ejecutable), `references/` (documentación adicional) y `assets/` (plantillas, imágenes, tablas). *"Skills follow the Agent Skills specification, a platform-agnostic standard."* **Es el activo más resistente del proyecto: sobrevive aunque se cierre toda la ruta gratuita.** `references/` es el sitio natural para la doctrina de hechos, sin cargarla al contexto hasta que haga falta. | https://claude.com/docs/skills/overview · https://claude.com/docs/skills/how-to |
| **El nombre del directorio debe coincidir con el campo `name`** | VERIFICADO | `name`: máximo 64 caracteres, minúsculas, números y guiones. | https://claude.com/docs/skills/how-to |
| **La descripción está limitada a 200 caracteres en claude.ai** | VERIFICADO — restricción de diseño real | *"Claude.ai limits descriptions to 200 characters. The Agent Skills specification allows up to 1024."* **La descripción de `fact-builder` tiene que caber en 200 caracteres y aun así disparar de forma fiable.** | https://claude.com/docs/skills/how-to |
| **La vía de subida a claude.ai acepta SOLO SEIS campos de frontmatter** | VERIFICADO — crítico | Permitidos: `allowed-tools`, `compatibility`, `description`, `license`, `metadata`, `name`. Cualquier otro produce error de validación. **Quedan fuera los campos propios de Claude Code**: `when_to_use`, `disable-model-invocation`, `paths`, `disallowed-tools`, `argument-hint`. Si el skill debe funcionar en las dos superficies, hay que escribirlo con estos seis y nada más. | https://code.claude.com/docs/en/skills |
| **Funciones del cuerpo que NO funcionan fuera de Claude Code** | VERIFICADO — **degradación silenciosa** | *"Claude Code-only body features, such as dynamic context injection, don't function in claude.ai chat or through the API."* En Cowork, cada línea `!` se sustituye por un placeholder. **Si `fact-builder` intentara leer el expediente con una línea de shell, en Cowork no se ejecutaría y trabajaría sobre nada, sin avisar.** | https://code.claude.com/docs/en/skills |
| **Consumo de contexto (divulgación progresiva)** | VERIFICADO | *"Claude reads skill names and descriptions at startup (~100 tokens each)"*; el SKILL.md completo se carga al activarse; `references/` y `scripts/` solo cuando hacen falta. Recomendación: *"Keep your main SKILL.md under 500 lines."* **Compiten poco en reposo y mucho al activarse: la doctrina larga va en `references/`, no en el cuerpo.** | https://claude.com/docs/skills/overview |
| **Advertencia de seguridad de la propia documentación** | VERIFICADO | No incrustar claves ni contraseñas, y **revisar toda skill descargada antes de habilitarla**. | https://claude.com/docs/skills/how-to |

### 4.3 — Cómo se instala: las vías, con su plan

| Vía | Plan | Etiqueta | Pasos y barreras | Fuente |
|---|---|---|---|---|
| **Subir un ZIP en Customize > Skills** (sin administrador, sin repositorio, sin terminal) | **Plan DUDOSO** (§4.1); la mecánica es VERIFICADA | VERIFICADO (mecánica) | Seis pasos: empaquetar la carpeta como ZIP → Customize > Skills → botón "+" → "+ Create skill" → "Upload a skill" → subir → activar. **Error de instalación más probable en manos no técnicas:** *"Correct structure: my-skill.zip └── my-skill/ ├── SKILL.md"* frente a *"Incorrect structure: files directly in ZIP root"*. **La guía de entrega debe traer el ZIP ya construido, no instrucciones para construirlo.** Las skills subidas son *"private to your individual account"*. Existe un límite de tamaño del ZIP (*"ZIP file exceeds size limits"*) **cuya cifra no está publicada**. | https://support.claude.com/en/articles/12512180-use-skills-in-claude |
| **Instalar un plugin desde nuestro repositorio git como marketplace** | **Todos los planes de pago** | VERIFICADO (3/3) — **vía recomendada** | Cowork: Customize > Plugins > "Add marketplace", aceptando la URL de GitHub o el atajo propietario/repositorio. Claude Code: `/plugin marketplace add`, luego `/plugin install`. Botón **Update** para traer la última versión. **Sin administrador, sin revisión, sin catálogo público.** Barreras: privacidad solo en GitHub; en GitLab y Bitbucket el repositorio debe ser público. Repositorios privados: verificado **solo en Claude Code** (*"Claude Code supports installing plugins from private repositories"*); **para Cowork es NOT FOUND — no inferir, hay que probarlo.** | https://claude.com/docs/cowork/guide/plugins · https://code.claude.com/docs/en/plugin-marketplaces |
| **Un directorio de skill puede convertirse en plugin añadiendo un manifiesto** | NO DECLARADO por plan | VERIFICADO | *"Any folder under a skills directory that contains a .claude-plugin/plugin.json manifest is loaded as a plugin."* **Permite que `fact-builder` empiece como skill simple y crezca a plugin con el MCP del Core sin reescribir nada ni cambiar de formato de distribución.** | https://code.claude.com/docs/en/plugins-reference |
| **Grabar un skill demostrando la tarea** | Pro, Max, Team | **DESCARTADO para su equipo** | *"Recording a skill is available… in Cowork in Claude for Mac. It isn't available in chat, on Windows, or on Free and Enterprise plans."* **Ella trabaja en Windows: hay que descartarla del plan y no mencionarla como opción**, aunque habría sido la vía más natural para que capturara sus propios flujos. | https://support.claude.com/en/articles/12512198-how-to-create-custom-skills |
| **Pedirle a Claude que guarde un skill desde la conversación** | NO DECLARADO | **INCONCLUSIVE — merece prueba empírica** | *"create and upload their own skills, including by asking Claude to save one in a conversation."* La afirmación aparece en la página de Claude Desktop para despliegues de terceros, **no en la documentación de producto general ni en los artículos de soporte**. Si se confirma, sería la vía de instalación más barata de todas. | https://claude.com/docs/third-party/claude-desktop/extensions |
| **Activar un skill pegándolo en el chat** | — | **NOT FOUND — decisivo para la guía** | Ninguna de las seis páginas oficiales consultadas lo describe. **No podemos decirle que pegue `fact-builder` en el chat y funcione como skill.** Pegar el texto hará que Claude lo lea como instrucciones de esa conversación, que no es lo mismo, y no debemos presentarlo como equivalente. | https://support.claude.com/en/articles/12512180-use-skills-in-claude |

### 4.4 — Trampas de nombres y de superficie

| Hecho | Etiqueta | Por qué importa | Fuente |
|---|---|---|---|
| **Un conflicto de nombre hace desaparecer el skill SIN error visible** | VERIFICADO | Un skill sincronizado desde claude.ai **se omite** si su nombre coincide con cualquier otro comando, y se ejecuta el otro. La comparación ignora mayúsculas, espacios y caracteres invisibles. **Distribuirlo dentro de un plugin elimina el riesgo por completo:** *"Plugin skills use a plugin-name:skill-name namespace, so they can't conflict with other levels."* | https://code.claude.com/docs/en/skills |
| **Precedencia** | VERIFICADO | Enterprise sobre personal, personal sobre proyecto. | https://code.claude.com/docs/en/skills |
| **Las skills de un plugin sí funcionan en las tres superficies; hooks y sub-agentes no** | VERIFICADO | *"Hooks and sub-agents run only in Cowork, so they appear grayed out in chat."* | https://support.claude.com/en/articles/13837440-use-plugins-in-claude |
| **¿Se usan los plugins en el chat?** | **INCONCLUSIVE** | *"Plugins are available in Cowork and Code. They aren't used in Chat"* frente al artículo de soporte que los lista funcionando en el chat web y en la pestaña Chat del escritorio (§7.7). **Cierra la última puerta imaginable de aprovechar un plugin sin Cowork.** | https://claude.com/docs/cowork/guide/plugins |
| **Las skills se pueden invocar dentro de los complementos de Office** | VERIFICADO | *"Skills you've enabled in your Claude settings are available in all Claude for M365 add-ins."* Escribir `/` en la barra lateral muestra las disponibles para esa aplicación. **`/fact-builder` sobre el documento abierto en Word es la capacidad más cercana a su forma real de trabajar** — pero exige plan de pago. Los complementos **consumen** skills, no permiten instalarlas. | https://claude.com/docs/office-agents/connectors-and-skills |
| **Coste de contexto visible antes de instalar** | VERIFICADO (en Claude Code) | El panel de detalle muestra *"a Context cost estimate so you can see how many tokens the plugin will add to your context window every turn"* y una sección "Will install". **Nos permite medir y declarar el coste de contexto de nuestro propio plugin antes de entregarlo, en lugar de estimarlo.** | https://code.claude.com/docs/en/discover-plugins |
| **Enviar al directorio oficial exige repositorio PÚBLICO y organización** | VERIFICADO | *"The repo must be public—closed-source plugins are not accepted."* Por claude.ai exige Team o Enterprise; un autor individual puede enviarlo desde Console. **No nos hace falta y conviene evitarlo.** | https://claude.com/docs/plugins/submit |
| **Skills provisionadas por la organización** | Team y Enterprise | VERIFICADO — no aplicable hoy | Solo importaría si el despacho creciera a plan Team. | https://claude.com/docs/skills/overview |

---

## §5 — Almacenamiento y ofimática sin costo

### 5.1 — Los conectores de nube: la vía que parecía la respuesta y no lo es

**Los conectores de Google Workspace están REFUTADOS como capacidad gratuita con escritura.** Cae por dos vías independientes, cualquiera de las cuales basta:

**(a) La escritura está negada en la propia documentación, con independencia del plan.**
- Gmail: *"Claude cannot create, send, or modify emails"* · *"Embedded images in emails are not visible to Claude"* — https://claude.com/docs/connectors/google/gmail
- Calendar: *"Claude cannot create, modify, or delete calendar events"* · *"Claude cannot send calendar invitations"* — https://claude.com/docs/connectors/google/calendar

**(b) El plan: cuatro fuentes en contra.** Las tres páginas de docs dicen *"Available on Pro, Max, Team, and Enterprise plans"*, y el tutorial de conectores abre con *"Prerequisites: A Claude account (Pro, Max, Team, or Enterprise for most connectors)"* — https://claude.com/docs/connectors/getting-started.md

**(c) Y aunque ambas se resolvieran a favor, el conector de Drive sería inservible para un expediente:** solo lee Google Docs. *"Google Sheets ❌ Not currently supported"*, *"Google Slides ❌ Not currently supported"*, máximo 10 MB, *"text extraction only"*, sin imágenes, sin comentarios ni sugerencias. **No lee .docx, no lee .xlsx, no lee PDF.** — https://claude.com/docs/connectors/google/drive

Un artículo de soporte afirma lo contrario en todo (*"available for all users on Claude and Claude Desktop"*, con *"Read Sheets, Slides, PDFs, images, and MS Office files"*, *"Send, reply to, and forward emails"*, *"Create, update, and delete events"*), y en la sesión de verificación se observaron herramientas de Drive con escritura presentes. **Eso corrobora que la capacidad existe en alguna configuración, pero no en qué plan ni con qué alcance.** La contradicción queda registrada en §7.3 y §7.4. **Dos refutadores la tumban; el tercero la deja dudosa. Gana la restrictiva: no se puede prometer.** — https://support.claude.com/en/articles/10166901-use-google-workspace-connectors

**Microsoft está cerrado por una barrera distinta y más dura, y no es de plan:** *"The Microsoft 365 connector requires a Microsoft Entra tenant tied to a Microsoft Business plan. Personal Microsoft accounts (such as @outlook.com or @hotmail.com addresses) can't be used to connect"*, más *"A Microsoft Entra Global Administrator in your tenant needs to authorize the integration."* — https://support.claude.com/en/articles/12542951-set-up-the-microsoft-365-connector

**Slack repite el mismo patrón**, escondido dentro de una viñeta de la columna Free de la página de precios: un administrador del espacio de trabajo debe aprobar la app de Claude en el Slack App Marketplace; sin permisos, el usuario solo ve "Request to install". **Una abogada independiente no es administradora de ningún Slack ajeno.** — https://support.claude.com/en/articles/11176164-use-connectors-to-extend-claude-s-capabilities

**Diferencia que sí importa a favor de Google:** ninguna página oficial excluye las cuentas personales @gmail.com ni exige administrador para una cuenta personal. Las instrucciones dicen *"Sign in to your Google account"*, y el único paso de administrador documentado (*"Your Google Workspace admin may need to allow Claude as a trusted application"*) aparece como resolución de problemas y presupone pertenecer a una organización Workspace. **Rigor obligado: la ausencia de una prohibición no es una autorización expresa. Se marca NOT FOUND respecto de la restricción, no VERIFICADO respecto del permiso.** — https://support.claude.com/en/articles/10166901-use-google-workspace-connectors

**No existe conector dedicado de OneDrive** independiente del de Microsoft 365, ni documentación oficial de Dropbox, Box o Notion con su plan. [NOT FOUND]

### 5.2 — La vía de la carpeta local sincronizada

Es la vía que **esquiva los conectores por completo**: si el contenido de la nube está en una carpeta corriente de Windows, cualquier programa la abre sin OAuth, sin conector y sin plan. **La pieza de sincronización es gratuita; lo que no es gratuito es Claude leyendo esa carpeta.**

| Pieza | Etiqueta | Qué está verificado, qué no | Fuente |
|---|---|---|---|
| **Google Drive para escritorio, modo ESPEJO** | VERIFICADO (el comportamiento) — **DUDOSO en lo demás** | *"Mirrored files will always be stored on your computer and in the cloud. They are always available offline."* **Recomendación operativa: usar espejo, no streaming** — en streaming los archivos viven en una unidad virtual, no en una carpeta normal, y solo se descargan al abrirlos. **La página citada NO afirma gratuidad, ni tipo de cuenta, ni ausencia de administrador**: tres extremos del inventario previo se apoyaban en una fuente que no los contiene. Evidencia lateral a favor: Google dice que el problema de administrador aparece *"If you use a work or school account"*, no con cuentas personales. Requiere Microsoft WebView2 (presente de fábrica en Windows 11). El espejo **exige tanto espacio en disco local como ocupe el Drive**. | https://support.google.com/drive/answer/13401938?hl=en |
| **OneDrive en Windows con cuenta Microsoft PERSONAL** | VERIFICADO (la cuenta personal) — **DUDOSO el "copia real en disco"** | El asistente pide *"your Microsoft personal account or work or school account"*: **no exige tenant de Entra ni administrador**. Esto **CORRIGE una conclusión anterior del proyecto: lo descartado era el CONECTOR de Microsoft 365, no el contenido del OneDrive personal.** Barrera técnica que invalida la premisa central si no se maneja: con **Files On-Demand, activo por defecto**, los archivos son marcadores en línea y **no ocupan disco** — *"without having to download all of them and use storage space"*. Solo están realmente en local si se marcan "Mantener siempre en este dispositivo". | https://support.microsoft.com/en-us/office/sync-files-with-onedrive-in-windows-615391c4-2bd3-4aae-a42a-858262e42a49 |
| **Cowork sobre esa carpeta** | **DE PAGO** | Es el eslabón que cuesta dinero. Y sobre unidades de red: rutas mapeadas a letra sí, **UNC crudas no**, y la unidad debe estar montada antes de arrancar el sandbox. | https://claude.com/docs/third-party/claude-desktop/local-access |

**Los techos de almacenamiento gratuito son pequeños y compartidos, y ahí la ruta "sin costo" se convierte en una suscripción:**
- Google: *"Each Google Account includes up to 15 GB of storage, which is shared across Gmail, Google Drive, and Google Photos."* Al llenarse, **no solo deja de subir archivos: deja de recibir correo en Gmail.** — https://support.google.com/drive/answer/6374270
- Microsoft: *"With a free Microsoft account, you have 5 GB of free cloud storage shared across your files and photos in OneDrive, attachments in Outlook.com."* Ampliarlos ya no se vende suelto: exige suscripción a Microsoft 365. — https://support.microsoft.com/en-us/onedrive/microsoft-storage-quotas

**Un archivo de expedientes escaneados agota 5 GB o 15 GB con facilidad.** Ese es el punto exacto donde la ruta gratuita de almacenamiento deja de serlo.

### 5.3 — Ofimática sin costo, y qué se pierde

| Pieza | Etiqueta | Qué da y qué cuesta | Fuente |
|---|---|---|---|
| **Claude genera .docx, .xlsx con fórmulas, .pptx y .pdf en Free** | VERIFICADO (3/3) — **el cimiento de la ruta gratuita** | Cero requisitos externos: ni Microsoft 365, ni Google Workspace, ni administrador, ni instalación. Recibe minutas, memoriales, cuadros de pruebas y liquidaciones funcionales sin pagar nada a nadie. Techo: 30 MB por archivo, y **cada archivo generado cuesta más cuota que una respuesta de texto**. | https://support.claude.com/en/articles/12111783-create-and-edit-files-with-claude |
| **Word, Excel y PowerPoint para la web, gratuitos con cuenta Microsoft** | VERIFICADO (3/3) | Para abrir y **corregir a mano** lo que Claude genere, sin comprar Office. 5 GB incluidos. | https://support.microsoft.com/en-us/office/what-s-the-difference-between-a-paid-microsoft-365-subscription-and-the-free-web-apps-7c813f33-d3bf-4e5b-9b92-dcab8ae910d2 |
| **Lo que se pierde con las versiones web gratuitas** | VERIFICADO — barreras no previstas | (1) **No hay modo solo-local**: *"Any documents you create with the free versions of apps like Word, Excel, and PowerPoint are automatically saved to OneDrive."* **Corregir a mano un escrito judicial en la versión web deposita material amparado por secreto profesional en la nube de Microsoft por defecto, sin decisión consciente.** (2) *"Security updates, but no new features"* — están congeladas. (3) Sin funciones de IA, sin aplicaciones de escritorio, sin soporte técnico. (4) Edición solo básica en pantallas menores de 10,1 pulgadas. (5) Menos funciones que las instaladas: puede morder en control de cambios avanzado, combinación de correspondencia y macros. **Sirve como corrector final, no como suite de trabajo.** | misma fuente |
| **Guardar lo generado directamente en Google Drive** | **INCONCLUSIVE** | *"you can download the files Claude creates or save them directly to Google Drive."* El artículo **no declara requisito de plan**, pero funcionalmente depende del conector de Drive, cuyo plan está en disputa. **Guardar en OneDrive: NOT FOUND — no está documentado.** **La ruta de entrega garantizada sigue siendo la descarga a su propio disco.** | https://support.claude.com/en/articles/12111783-create-and-edit-files-with-claude |
| **Complemento Claude para Word** | **DE PAGO, sin versión gratuita** | *"Claude for Word is generally available to Pro, Max, Team, and Enterprise plans."* Citas por sección clicables, edición preservando estilos, **control de cambios revisable en el panel nativo de Word**, hilos de comentarios, resumen del redlining de la contraparte, relleno de plantillas. **Es la capacidad más valiosa del inventario para su oficio.** Dato poco advertido: *"Word on the web"* figura entre las versiones soportadas **sin exigir suscripción a Microsoft 365** — el requisito de M365 se enuncia solo para Word en Windows. **El obstáculo para ella no es Microsoft: es el plan de Claude.** No corre en Word 2016/2019 perpetuo, ni iPad, ni Android. Archivos .doc heredados no soportados. Advertencia expresa de inyección de instrucciones con documentos de la contraparte. | https://claude.com/docs/office-agents/word |

---

## §6 — Límites reales: ¿aguanta una jornada de trabajo de verdad?

**Respuesta directa, sin suavizar: no se puede afirmar que la ruta gratuita aguante una jornada real de trabajo sobre un expediente, y todos los indicios apuntan a que no.** La ruta gratuita sirve para redactar piezas sueltas. No sirve para sostener un expediente.

### 6.1 — Los dos números que decidirían no existen en público

| Dato | Etiqueta | Qué consta |
|---|---|---|
| **Cuántos mensajes, tokens o páginas permite Free** | **NOT FOUND** | Ninguna página oficial lo publica. **Cualquier estimación sería inventada.** |
| **Ventana de contexto del plan Free** | **NOT FOUND** | El artículo que la explica se titula literalmente *"How large is the context window on paid Claude plans?"* y todas sus cifras (1M, 500K, 200K) se declaran *"on all paid plans"*. **Free no aparece.** Es exactamente el número que determina si caben veinte anexos. — https://support.claude.com/en/articles/8606394-how-large-is-the-context-window-on-paid-claude-plans |
| **¿Free tiene límite semanal?** | **NOT FOUND** | Los artículos de Pro y Max declaran expresamente que **esos** planes añaden tope semanal. Ninguna página lo afirma ni lo niega para Free. **No debe afirmarse ni negarse: es una laguna documental, no un hecho.** |
| **Cuánto más consume Cowork que el chat** | **NOT FOUND** | Se declara cualitativamente (*"consumes more"*, *"Higher intensity"*, *"many more tokens than chat"*) **nunca con un multiplicador numérico.** |
| **Cifra del límite semanal de Cowork** | **NOT FOUND** | Se confirma que existe (el changelog corrige un fallo *"after the weekly Cowork limit was used up"*) pero no hay número. Solo se consulta en Settings > Usage de la propia cuenta. |

### 6.2 — Lo único cuantificado, y no es tranquilizador

- **Pro da *"at least five times the usage per session compared to our free service"***. Leído al revés: **Free tiene como mucho una quinta parte del uso por sesión de Pro.** Y la propia documentación advierte que Cowork puede agotar el límite de Pro con trabajo real. — https://support.claude.com/en/articles/8325606-what-is-the-pro-plan
- **Ventana de sesión: cinco horas.** Al agotarla, el mensaje literal es *"5-hour limit reached - resets [time]"*, precedido de *"Approaching 5-hour limit."* Las opciones son *"wait for it to reset, upgrade your plan, or purchase usage credits"* — y **en Free la tercera no existe.** Un tope agotado a media mañana no se recupera hasta cinco horas después. **Con audiencia o vencimiento de término, eso es un riesgo operativo que hay que diseñar, no descubrir.** — https://support.claude.com/en/articles/11647753-how-do-usage-and-length-limits-work
- **Un solo depósito para todas las superficies:** *"Your usage of all different Claude product surfaces (claude.ai, Claude Code, Claude Desktop) counts towards the same usage limit."* **Instalar el escritorio no añade capacidad; le da otra puerta al mismo depósito.**

### 6.3 — Cinco barreras estructurales que nadie había listado

1. **La cuota gratuita es elástica a la baja y no es un número.** *"The number of messages you can send will vary based on demand, and we may impose other types of usage limits to ensure fair access to all users."* **Anthropic se reserva expresamente encogerla e imponer límites nuevos. Ninguna planificación de jornada es posible sobre una cuota que cambia sola.** — https://support.claude.com/en/articles/8114491-get-started-with-claude

2. **Pro compra explícitamente prioridad en hora punta.** Entre lo que Pro añade figura *"Priority access during high-traffic periods"*. Traducido: **el plan gratuito está deprioritizado precisamente en horario laboral**, que es cuando ella trabaja. La degradación no es aleatoria: coincide con el peor momento posible, la víspera de un término.

3. **Existe un muro de capacidad independiente de la cuota.** *"Due to unexpected capacity constraints, Claude is unable to respond…"* **Puede quedarse sin servicio aun sin haber agotado su límite**, y la documentación aclara que esto ni siquiera aparece en la página de estado. — https://support.claude.com/en/articles/12466728-troubleshoot-claude-error-messages

4. **Los anexos no se pagan una vez: encarecen toda la conversación posterior.** *"The number of messages you can send will vary based on message length, including the length of files you attach, the length of your current conversation."* Subir veinte anexos **sube el precio de cada mensaje que venga después**. El costo crece de forma compuesta a lo largo de la jornada. Y la guía de errores lo delata desde el otro lado: la solución oficial al exceso es *"Removing attachments or files."*

5. **Lo más útil es también lo más caro.** La documentación enumera como factores de consumo: *"Message length, File attachment size, Current conversation length, Tool usage (e.g., Research, web search), Model choice, Effort level, Artifact creation and usage."* **Las tres cosas que de verdad le sirven a una abogada — crear archivos, buscar en la web y mantener una conversación larga sobre un caso — son también las tres que más cuota queman.** El sistema encarece el trabajo profundo, que es el único que le sirve. — https://support.claude.com/en/articles/9797557-usage-limit-best-practices

### 6.4 — Los techos que ella tocará primero

| Techo | Cifra | Cuándo duele |
|---|---|---|
| **Proyectos en Free** | **5** | Una abogada independiente con más de cinco asuntos activos choca el primer mes. Sin vía de ampliación sin pagar. |
| **Conectores personalizados en Free** | **1** | Hay que decidir si ese único cupo se gasta en el Core del producto o en otra cosa. **No caben ambos.** |
| **Archivos por chat** | **20** | Un expediente de litigio los supera con facilidad. Ese es el punto donde la ruta gratuita empieza a doler. |
| **Archivo dentro de un proyecto** | **30 MB** | Es el tope real de la superficie pensada para organizar casos de forma persistente, no los 500 MB del chat. |
| **Archivo creado o descargado** | **30 MB** | Un PDF con anexos escaneados lo supera. |
| **Archivo que Cowork lee** | **50 MB** | Un solo PDF escaneado de un expediente puede superarlo. |
| **Análisis visual de PDF** | **100 páginas** | Por encima, solo texto — y un escaneado no tiene texto. **Hay que partir en bloques de 100.** |
| **Máximo de páginas de PDF** | **1000** | Pero es el tope del ingestor: **ningún PDF de 1000 páginas cabe siquiera en los 200K tokens de los planes de pago.** |
| **Imágenes por mensaje** | **20**, 10 MB cada una, 8000×8000 px | Fotos de folios y actas. Con la advertencia de alucinación en imágenes de baja calidad o rotadas. |
| **RAG del conocimiento de proyecto** | **De pago** | En Free todo debe caber crudo en la ventana de contexto, **y la degradación es silenciosa**. |
| **Almacenamiento de terceros** | **5 GB** (OneDrive) / **15 GB compartidos** (Google) | Un archivo de expedientes escaneados los agota. |

### 6.5 — Lo que sí se puede afirmar sobre la jornada

**Con plan Pro pagado**, el riesgo no desaparece, solo cambia de forma: Cowork es la superficie **más cara en consumo** por declaración del propio fabricante, existe un límite semanal cuya cifra no se publica, y las mitigaciones oficiales son organizativas, no técnicas — agrupar trabajo relacionado en una sola sesión, usar el chat normal para tareas simples, y vigilar el consumo en Settings > Usage. Los comandos `/usage` y `/cost` dentro de Cowork permiten medirlo sin gastar cuota. **Los créditos de uso son la única válvula real, y son gasto abierto a tarifas de API.**

**La conclusión honesta que hay que darle a los dueños: la capacidad no se puede prometer, se tiene que medir.** Hay que instrumentar una jornada real con su carga real — un expediente representativo, sus formatos, sus escaneados — y observar dónde se rompe, antes de comprometer cualquier proceso que dependa de la plataforma en fecha de vencimiento.

---

## §7 — Contradicciones en la documentación oficial

Diecisiete puntos donde dos o más páginas oficiales de Anthropic se contradicen. **Ninguna se puede resolver leyendo más documentación.** Cada una lleva sus URLs.

**7.1 — Plan mínimo para usar Skills. La más costosa para este encargo.**
- *"Skills are available for users on **Pro, Max, Team, and Enterprise** plans."* — https://claude.com/docs/skills/overview
- *"Skills are available for users on **Free**, Pro, Max, Team, and Enterprise plans."* — https://support.claude.com/en/articles/12512180-use-skills-in-claude (misma frase en https://support.claude.com/en/articles/12512176-what-are-skills y https://support.claude.com/en/articles/12512198-how-to-create-custom-skills)
- **No hay árbitro:** "Skills" no aparece en ninguna viñeta de https://claude.com/pricing, ni de Free ni de Pro.

**7.2 — Plan de las extensiones de escritorio (MCPB). La más grave para la ruta gratuita**, porque son la única vía candidata a acceso local sin costo.
- *"Available for **Team and Enterprise** plans with Claude Desktop."* — https://claude.com/docs/connectors/custom/desktop-extensions
- *"Desktop extensions are available to **all users** on Claude Desktop."* — https://support.claude.com/en/articles/11176164-use-connectors-to-extend-claude-s-capabilities
- Viñeta del plan **GRATUITO**: *"Unlock more from Claude with desktop extensions"* — https://claude.com/pricing
- Cuarto y quinto datos, ambos sin restricción de plan: el artículo de MCP locales describe la instalación desde el directorio y de extensiones propias sin mencionar plan — https://support.claude.com/en/articles/10949351-getting-started-with-local-mcp-servers-on-claude-desktop — y la página de MCP Apps describe configurar servidores MCP locales vía Settings > Developer sin restringir plan — https://claude.com/docs/connectors/building/mcp-apps/getting-started
- **Matiz que un refutador aportó y que cambia el peso sin resolverlo:** leída entera, la página de docs trata de **despliegue empresarial** con lista blanca administrada (*"Enterprise deployment: For Team and Enterprise plans, admins can…"*), lo que hace plausible que su nota de plan gobierne el **empaquetado y gobierno corporativo**, no la instalación individual.

**7.3 — Plan de los conectores de Google Workspace.**
- *"Available on **Pro, Max, Team, and Enterprise** plans."* en las tres páginas: https://claude.com/docs/connectors/google/drive · https://claude.com/docs/connectors/google/gmail · https://claude.com/docs/connectors/google/calendar
- *"Google Workspace connectors (Gmail, Google Calendar, and Google Drive) are available for **all users** on Claude and Claude Desktop."* — https://support.claude.com/en/articles/10166901-use-google-workspace-connectors
- Viñeta dentro del plan **Free**: *"Connect Slack and Google Workspace services"* — https://claude.com/pricing
- Cuarta fuente contra Free, en la línea de prerrequisitos del tutorial: *"A Claude account (Pro, Max, Team, or Enterprise for most connectors)"* — https://claude.com/docs/connectors/getting-started.md

**7.4 — Capacidad de escritura en Google Workspace. Negación expresa contra afirmación expresa.**
- Docs: *"Claude cannot create, send, or modify emails"* — https://claude.com/docs/connectors/google/gmail · *"Claude cannot create, modify, or delete calendar events"* y *"Claude cannot send calendar invitations"* — https://claude.com/docs/connectors/google/calendar · *"Google Sheets ❌ Not currently supported"*, *"Up to 10MB, text extraction only"* — https://claude.com/docs/connectors/google/drive
- Soporte: *"Send, reply to, and forward emails"*, *"Create, update, and delete events"*, *"Read Sheets, Slides, PDFs, images, and MS Office files"*, *"Share, move, and trash files"*, *"Create folders"* — https://support.claude.com/en/articles/10166901-use-google-workspace-connectors

**7.5 — Tareas programadas y carpetas locales. Contradicción INTERNA, en la misma página.**
- *"They can't be tied to a folder on your computer"* junto a *"If a scheduled task requires local files or apps, it will only run locally"*, y la creación manual incluye una carpeta opcional — https://support.claude.com/en/articles/13854387-schedule-recurring-tasks-in-claude-cowork
- El changelog refuerza el lado local con el ajuste "Run this task while your Mac sleeps" y un fallo de ejecuciones duplicadas al despertar el equipo — https://claude.com/docs/cowork/changelog
- **Causa probable localizada por un refutador:** *"Scheduled tasks run remotely"* — corren en la nube, y por eso no pueden tocar disco.

**7.6 — ¿Cowork trabaja en su computador o en la nube?**
- Página de producto: *"Works directly on your computer — Claude reads and writes local files without requiring manual uploads or downloads."* — https://claude.com/docs/cowork/overview
- Arquitectura: *"Cowork sessions run in the cloud by default… The agent's work, including any local files it opens through the desktop app, is processed on Anthropic's servers rather than staying on the device."* — https://support.claude.com/en/articles/14479288-claude-cowork-architecture-overview
- No son estrictamente incompatibles, **pero la página que vende el producto omite el hecho decisivo para una abogada: por defecto el material del expediente sale del dispositivo.**

**7.7 — ¿Se usan los plugins en el chat?**
- *"Plugins are available in Cowork and Code. They aren't used in Chat."* — https://claude.com/docs/cowork/guide/plugins (repetido en https://claude.com/docs/plugins/overview)
- El artículo de soporte los lista funcionando en el chat web y en la pestaña Chat del escritorio — https://support.claude.com/en/articles/13837440-use-plugins-in-claude

**7.8 — ¿Cowork tiene límite semanal PROPIO o comparte el contador general?**
- *"Fixed chat refusing new messages after **the weekly Cowork limit** was used up."* El artículo definido implica un límite específico de Cowork, y revela que agotarlo llegó a bloquear el chat — https://claude.com/docs/cowork/changelog
- *"Your usage of all different Claude product surfaces (claude.ai, Claude Code, Claude Desktop) counts towards **the same** usage limit."* — https://support.claude.com/en/articles/11647753-how-do-usage-and-length-limits-work

**7.9 — Tamaño máximo de archivo: cuatro cifras en cuatro páginas.**
- *"The maximum file size is **30MB** per file for both uploads and downloads."* — https://support.claude.com/en/articles/12111783-create-and-edit-files-with-claude
- *"File size: **500MB** per file"* para chats, y 30 MB para archivos de proyecto — https://support.claude.com/en/articles/8241126-upload-files-to-claude
- *"Claude reads individual files up to **50 MB**."* — https://claude.com/docs/cowork/guide/projects
- Pueden describir superficies distintas, **pero la frase "for both uploads and downloads" es incompatible con "500MB per file" para subidas.** Consecuencia práctica: **no se le puede decir cuánto pesa el expediente más grande que puede subir.**

**7.10 — Sistemas operativos de Dispatch.**
- *"Dispatch requires a Pro or Max plan and the latest Claude Desktop app on **macOS or Windows**."* — https://claude.com/docs/cowork/guide/dispatch
- *"The latest Claude Desktop app installed and running (macOS, Windows x64, **or Linux**)"* — https://support.claude.com/en/articles/13947068-assign-tasks-from-anywhere-in-claude-cowork

**7.11 — ¿Existe Cowork en el plan Free?**
- *"Cowork is available to paid Claude plans (Pro, Max, Team, Enterprise) **only**."* — https://support.claude.com/en/articles/13345190-get-started-with-claude-cowork
- *"Custom connectors using remote MCP are available on Claude, **Cowork**, and Claude Desktop for users on **free**, Pro, Max…"* — https://support.claude.com/en/articles/11176164-use-connectors-to-extend-claude-s-capabilities
- **Los tres refutadores coinciden en que la segunda frase enumera superficies y planes por separado, y no otorga Cowork a Free.** Se registra por su redacción confusa, no como contradicción de fondo. **Manda la restricción.**

**7.12 — Fable en el plan gratuito y créditos de uso.**
- La tabla de modelos consigna para Fable, en la columna Free, la entrada *"Usage credits"* — https://claude.com/pricing
- *"Usage credits allow individuals subscribed to **paid** Claude plans (Pro, Max 5x, and Max 20x)"*, sin mencionar Free como elegible — https://support.claude.com/en/articles/12429409-manage-usage-credits-for-paid-claude-plans
- **Advertencia de proveniencia:** la lectura de esa tabla fue indirecta (resumen del contenido de la página, no inspección visual). Podría ser un error de lectura. Se marca como contradicción **a confirmar**, no como hecho firme.

**7.13 — Formato de `.mcp.json` para servidores MCP locales.**
- *"To distribute a local server… bundle it in a plugin using `.mcp.json`."* — https://claude.com/docs/connectors/overview
- La única especificación del archivo localizada describe entradas que usan *"`type` (`http` or `sse`), not `transport`, and supports `url`, `headers`, and `oauth` only"* — **ningún proceso local stdio** — https://claude.com/docs/third-party/claude-desktop/extensions
- **O el formato de primera parte es distinto y no está documentado, o la afirmación de la página de conectores es imprecisa.**

**7.14 — Límites de plugins por marketplace: dos juegos de cifras sin advertencia.**
- *"Plugins per marketplace: **500**"*, *"Plugin package size (uncompressed): **200 MB**"* — https://claude.com/docs/cowork/guide/plugins
- *"Max plugin ZIP size (upload): **50 MB**"*, *"Max plugins per marketplace (manual): **100**"*, *"…(GitHub sync): 500"* — https://support.claude.com/en/articles/13837433-manage-plugins-for-your-organization
- Solo son conciliables si unas son subida manual por administrador y otras sincronización desde GitHub, **pero ninguna de las dos páginas advierte de esa distinción.** Citar la cifra equivocada lleva a un dimensionamiento erróneo.

**7.15 — Estado de la gestión de plugins por organización.**
- *"Org-wide sharing and management are **coming in the weeks ahead**."* — https://claude.com/docs/plugins/overview
- Ya documentado como existente: *"On Team and Enterprise plans, administrators can require certain plugins for everyone"* — https://claude.com/docs/cowork/guide/plugins — con artículo de soporte completo: https://support.claude.com/en/articles/13837433-manage-plugins-for-your-organization
- **La página de overview parece desactualizada; no debe usarse como fuente de disponibilidad.**

**7.16 — Conectores web "para todos" contra el plan de cada conector.**
- *"Web connectors are available for **all users** on Claude, Cowork, Claude Desktop, and Claude Mobile."* — https://support.claude.com/en/articles/11176164-use-connectors-to-extend-claude-s-capabilities
- El mismo artículo remite a la documentación de cada conector, que restringe Google Drive, Gmail y Calendar a Pro+. **La afirmación general y las páginas particulares no son consistentes entre sí.**

**7.17 — Laguna documental (no contradicción estricta, mismo efecto práctico).**
La página en la que se apoyó el diseño del proyecto, https://claude.com/docs/cowork/overview.md, **no declara requisito de plan ni de suscripción en ninguna línea de su texto completo**, mientras tres páginas oficiales coinciden en que Cowork exige plan de pago. **Un lector que se guíe solo por la documentación técnica concluye, erróneamente, que Cowork podría estar disponible sin costo.**

### 7.bis — Contradicciones que se RETIRAN

Los refutadores comprobaron que dos de las contradicciones que arrastraba el inventario **no existen**. Mantenerlas desacredita las que sí son reales.

1. **"La frase de conectores nombra Cowork junto a planes Free, luego Free tiene Cowork."** Falso: enumera las superficies donde existe la función y por separado los planes que pueden usarla. **Los tres refutadores coinciden.** Se conserva en §7.11 solo como aviso de redacción confusa.
2. **"Compartir un chat y publicar un artifact se contradicen sobre los adjuntos."** Son **dos mecanismos distintos**: compartir un CHAT no lleva los adjuntos; la frase sobre adjuntos de la página de artifacts se refiere a compartir un ARTIFACT. **Ambas pueden ser ciertas a la vez.** Dos refutadores la retiran; el tercero se niega a avalar la garantía sin lectura directa, por lo que la fila sigue marcada DUDOSA en §3.4 — **pero como cautela, no como contradicción.**

Y una afirmación que se **elimina por carecer de fuente**: *"el contenido cacheado en un proyecto no vuelve a contar contra el límite de uso"*. Un refutador revisó las dos páginas de proyectos y **no aparece en ninguna**. No debe repetirse.

---

## §8 — Lo que NO existe

**Para que nadie lo prometa.** Todo lo de esta lista se buscó y no se encontró, o se encontró negado expresamente.

### Capacidades que no existen en ninguna superficie ni plan

1. **Transcripción de un archivo de audio subido** (una entrevista grabada). Ningún formato de audio figura en la lista oficial de tipos admitidos, y el changelog completo de Claude Desktop no registra tal incorporación. **Es el dolor número uno declarado por la profesional y la plataforma no lo resuelve.** — https://support.claude.com/en/articles/8241126-upload-files-to-claude
2. **Formatos de vídeo en la subida de archivos.** No aparecen. (El changelog solo registra reproducción en línea de audio y vídeo en el visor de archivos del panel Code: eso es visualización, no transcripción.)
3. **OCR declarado para PDF escaneados en claude.ai.** La palabra OCR no aparece en la documentación consultada. Solo hay descripción del pipeline de visión, en documentación de plataforma cuya lista de superficies **no incluye claude.ai**.
4. **Citas con número de página en claude.ai.** La función se documenta para Claude API, AWS, Bedrock, Google Cloud y Microsoft Foundry. **claude.ai no figura.** Y para .docx y .xlsx no hay soporte de citas en absoluto. — https://platform.claude.com/docs/en/build-with-claude/citations
5. **Una función de traducción dedicada con garantías de fidelidad.** Solo capacidad conversacional multilingüe.
6. **Generación o edición de imágenes.** Declarado expresamente como limitación. — https://platform.claude.com/docs/en/build-with-claude/vision
7. **Grabar un skill en Windows.** *"It isn't available in chat, on Windows, or on Free and Enterprise plans."* — https://support.claude.com/en/articles/12512198-how-to-create-custom-skills
8. **Activar un skill pegándolo o adjuntándolo en la conversación.** Ninguna de las seis páginas oficiales sobre skills lo describe.
9. **Reglas de denegación por ruta para un usuario individual sin administrador.** El comportamiento documentado es *"Unrestricted"*.
10. **Interfaz en Cowork para crear, editar, limitar o asignar permisos a sub-agentes.** Lo que existe documentado en ese sentido pertenece a Claude Code.
11. **Conector dedicado de OneDrive** independiente del de Microsoft 365.
12. **Guardar los archivos generados directamente en OneDrive.** Solo se documenta descarga y guardado en Google Drive.
13. **Una lista oficial de los tipos de archivo que Cowork puede LEER del disco local.**
14. **Extensión de sistema de archivos instalable por autoservicio desde el directorio.** *"Local MCP servers distributed through third-party package registries like npm or PyPI cannot be listed directly in the Connectors Directory."* Alguien tiene que construirla y entregársela.

### Vías gratuitas que no existen

15. **Cowork, Claude Code, plugins, sub-agentes, hooks, Dispatch, tareas programadas, computer use, live artifacts, Research, búsqueda de chats pasados, RAG de proyecto y Claude en Chrome en el plan gratuito.** Ninguna. **En Free no existe ninguna vía agéntica de lectura y escritura sobre archivos locales.**
16. **Prueba gratuita, periodo de evaluación o descuento promocional vigente para Pro.** No se documenta ninguno.
17. **Un plan intermedio entre Free y Pro.** No existe. Y **Team está vetado por el mínimo de dos miembros**.
18. **Descuento por pago anual en Max.** Verificado que NO existe: *"The Max plan is currently available as a monthly subscription only."*
19. **Programa educativo, gratuito ampliado o de descuento aplicable a una PROFESIONAL INDEPENDIENTE del derecho.** Los cuatro localizados exigen perfiles que ella no tiene: educador K-12 verificado (https://www.anthropic.com/news/claude-for-teachers), universidad, organización sin ánimo de lucro **con mínimo dos asientos** (https://www.anthropic.com/news/claude-for-nonprofits), o mantenedor de código abierto de alto impacto (https://claude.com/contact-sales/claude-for-oss).

### Cifras que no existen en público

20. **Límites numéricos del plan gratuito**: mensajes, tokens, tareas u horas. **Ninguna.**
21. **Ventana de contexto del plan gratuito.**
22. **Si Free tiene o no límite semanal.**
23. **Cifras absolutas de los límites de Pro, Max 5x y Max 20x**: solo multiplicadores relativos.
24. **Cuantificación del sobreconsumo de Cowork frente al chat.**
25. **Cifra del límite semanal de Cowork.**
26. **Número máximo de tareas programadas, de proyectos de Cowork, de carpetas por proyecto, de skills habilitables, y de conectores personalizados en planes de pago.**
27. **Límite de tamaño del ZIP al subir un skill a claude.ai.** El error existe (*"ZIP file exceeds size limits"*), la cifra no.
28. **Límite de tamaño de la memoria de proyecto de Cowork.**
29. **Duración máxima de grabación en dictado y modo voz.**
30. **Precio en pesos colombianos.** Solo *"with pricing in your local currency where supported"*, sin confirmar que el peso colombiano esté entre las monedas soportadas.
31. **Requisitos mínimos de RAM, disco o versión de Windows para Cowork**, más allá de la característica Virtual Machine Platform.
32. **Retención y borrado de los datos de una sesión de Cowork EN LA NUBE para Pro y Max.** La única frase de retención localizada se refiere a compromisos comerciales de Team y Enterprise.
33. **Plan requerido para MCP Apps, para la búsqueda web y para el pensamiento extendido.** Ninguna de esas páginas lo declara.
34. **Criterios de elegibilidad del programa para organizaciones sin ánimo de lucro.**
35. **Contenido y disponibilidad por plan del directorio de conectores.** Es un catálogo vivo dentro del producto; la documentación no lo publica.

### Nota de proveniencia

- La URL https://support.claude.com/en/articles/14680753-extend-claude-cowork-with-third-party-platforms, que aparece en resultados de búsqueda, **devuelve HTTP 404**. No se pudo verificar su contenido.
- https://claude.com/docs/cowork/guide/skills.md **devuelve HTTP 404**. **No existe guía dedicada a skills en Cowork**: hay que reconstruir los pasos desde la página de overview y desde la documentación de Claude Code.
- Una afirmación de que *"Cowork is now available to Pro plan users on Claude Desktop (macOS only)"* procede de **un resumen de buscador, no de consulta directa**. No se toma como autoridad y probablemente describe un estado anterior del despliegue. El centro de ayuda declara macOS y Windows, y el changelog contiene decenas de correcciones específicas de Cowork en Windows.

---

## §9 — Preguntas abiertas

Numeradas, con lo que bloquea cada una. **Ninguna se resuelve leyendo más documentación.**

**P-1 — ¿Puede una cuenta Pro individual FORZAR que una sesión de Cowork corra en local en vez de en la nube?**
*Bloquea:* toda la propuesta de confidencialidad, y el funcionamiento del Core como MCP local (*"Local MCP servers don't run in sessions in the cloud"*). *Por qué está abierta:* el interruptor "Run Cowork in the cloud" solo se documenta como control de administrador en Team y Enterprise; para Pro y Max no se localizó control equivalente. *Cómo se cierra:* abriendo Cowork en una cuenta Pro y buscando el ajuste. **Es la pregunta empírica número uno del inventario.**

**P-2 — ¿Su equipo Windows 11 puede ejecutar Cowork?**
*Bloquea:* la recomendación de gasto. Pagar Pro no sirve de nada si el equipo no tiene virtualización. *Por qué está abierta:* exige comprobar que la característica Virtual Machine Platform esté disponible y activable, lo que requiere permisos de administrador local. *Cómo se cierra:* comprobándolo en su máquina **antes** de recomendar el pago.

**P-3 — ¿Las Skills funcionan en el plan gratuito?**
*Bloquea:* si el primer entregable (`fact-builder`) puede entregarse sin costo. *Por qué está abierta:* contradicción de una página de docs contra tres artículos de soporte, sin árbitro en la página de precios, y **los tres refutadores no llegan al mismo veredicto** (§7.1). *Cómo se cierra:* abrir una cuenta Free, activar la ejecución de código en Settings > Capabilities, y ver si aparece **Customize > Skills** con el botón de subir. **Un minuto y cero gasto.**

**P-4 — ¿Puede instalar una extensión de escritorio (MCPB) en el plan gratuito?**
*Bloquea:* la única vía candidata a acceso a archivos locales sin pagar. *Por qué está abierta:* contradicción a cinco bandas (§7.2). *Cómo se cierra:* intentar instalar un `.mcpb` en Claude Desktop con cuenta Free. **Advertencia que hay que dar junto con el resultado: aunque funcione, no basta.** Claude Desktop en Free es solo chat — sin bucle agéntico, sin hooks, sin sub-agentes, sin sesiones de fondo. **Acceso a disco no es agencia.**

**P-5 — ¿Un plugin puede traer un servidor MCP LOCAL en Cowork, y con qué formato exacto?**
*Bloquea:* la vía de instalación del Core sin administrador y sin MCPB. *Por qué está abierta:* la documentación afirma que se puede, pero la única especificación localizada del archivo solo admite `http` y `sse` (§7.13). *Cómo se cierra:* construyendo un plugin de prueba con un servidor stdio e instalándolo en Cowork.

**P-6 — ¿La actualización de las instrucciones de carpeta por parte de Claude requiere aprobación del usuario?**
*Bloquea:* la evaluación del riesgo de inyección persistente. Si Claude puede reescribir las instrucciones permanentes de una carpeta sin pedir permiso, un documento de contraparte con instrucciones ocultas podría alterar la conducta futura del sistema sobre ese expediente. *Por qué está abierta:* no documentado. *Cómo se cierra:* probándolo en una sesión con un documento de prueba.

**P-7 — ¿Qué formatos reales de su expediente lee Cowork, y cómo rinde con sus escaneados?**
*Bloquea:* cualquier promesa sobre trabajar el expediente en disco. *Por qué está abierta:* no existe lista oficial de formatos legibles; el tramo de más de 100 páginas apaga el análisis visual; los escaneados sin capa de texto no son citables. *Cómo se cierra:* probando con un expediente representativo real, incluidos PDF escaneados y `.doc` heredados.

**P-8 — ¿Cuánto aguanta realmente una jornada suya?**
*Bloquea:* cualquier proceso que dependa de la plataforma en fecha de vencimiento. *Por qué está abierta:* no existe ninguna cifra pública ni de Free ni de Pro, y la cuota gratuita varía con la demanda (§6). *Cómo se cierra:* **instrumentando una jornada real** con su carga real y observando dónde se rompe, usando `/usage` y `/cost` en Cowork y Settings > Usage. **No se puede estimar: hay que medirlo.**

**P-9 — ¿Puede activar los conectores de Google con su cuenta personal @gmail.com, y con qué alcance real?**
*Bloquea:* toda la vía de almacenamiento y correo. *Por qué está abierta:* contradicción de plan a cuatro bandas y de capacidad de escritura (§7.3, §7.4); y **la ausencia de prohibición de cuentas personales no es autorización expresa**. *Cómo se cierra:* intentando conectarlo con su cuenta y anotando qué herramientas aparecen realmente.

**P-10 — ¿Funciona un repositorio de GitHub PRIVADO como marketplace desde Cowork?**
*Bloquea:* si el material del producto puede mantenerse fuera del ojo público. *Por qué está abierta:* verificado solo en Claude Code; la página de Cowork menciona GitHub y GitHub Enterprise, y repositorios públicos en GitLab y Bitbucket, **pero no declara nada sobre repos privados**. *Cómo se cierra:* probándolo en su Cowork. **No inferir.**

**P-11 — ¿Se puede pedirle a Claude que guarde un skill desde la conversación?**
*Bloquea:* nada crítico, pero sería la vía de instalación más barata de todas. *Por qué está abierta:* la afirmación solo aparece en la página de Claude Desktop para despliegues de terceros, no en la documentación de producto general. *Cómo se cierra:* pidiéndoselo en una sesión.

**P-12 — ¿Existe dictado en escritorio y web, o sigue siendo solo móvil?**
*Bloquea:* la vía "hablar en vez de escribir", que es la adecuada para una usuaria sin habilidades técnicas. *Por qué está abierta:* el artículo de soporte dice *"when using Claude for iOS or Android"*, pero el changelog registra dictado en el compositor de escritorio y en el panel de Chrome. *Cómo se cierra:* mirando la versión instalada.

**P-13 — ¿Los planes de pago son contratables y facturables desde Colombia?**
*Bloquea:* la viabilidad de la única ruta agéntica verificada. *Por qué está abierta:* la lista de ubicaciones confirma que se puede **ACCEDER** a Claude desde Colombia, pero **no desglosa qué funciones ni qué planes están disponibles en cada país**, y no publica el precio en moneda local. *Cómo se cierra:* llegando a la pantalla de pago con su cuenta.

**P-14 — ¿Los adjuntos de una conversación viajan al compartir?**
*Bloquea:* la política de comparticiones del despacho, y por tanto el secreto profesional. *Por qué está abierta:* dos refutadores dan por disuelta la aparente contradicción; el tercero se niega a avalar una garantía de confidencialidad sin lectura directa. *Cómo se cierra:* comprobándolo con un chat de prueba con un adjunto inocuo. **Hasta entonces, asumir el peor caso.**

**P-15 — ¿Qué conectores tiene realmente disponibles en su cuenta?**
*Bloquea:* cualquier decisión de diseño que dependa de un conector. *Por qué está abierta:* el directorio es un catálogo vivo dentro del producto; la documentación no publica su contenido, y la consulta al registro desde el entorno de verificación devolvió vacío. *Cómo se cierra:* abriendo **Customize > Connectors** en su cuenta.

---

## §10 — Fuentes

Todas consultadas el 2026-08-25.

### Planes, precios y límites
- https://claude.com/pricing
- https://support.claude.com/en/articles/8325606-what-is-the-pro-plan
- https://support.claude.com/en/articles/8325609-how-do-i-sign-up-for-the-pro-plan
- https://support.claude.com/en/articles/11049741-what-is-the-max-plan
- https://support.claude.com/en/articles/9266767-what-is-the-team-plan
- https://support.claude.com/en/articles/8114491-get-started-with-claude
- https://support.claude.com/en/articles/11647753-how-do-usage-and-length-limits-work
- https://support.claude.com/en/articles/8606394-how-large-is-the-context-window-on-paid-claude-plans
- https://support.claude.com/en/articles/9797557-usage-limit-best-practices
- https://support.claude.com/en/articles/12429409-manage-usage-credits-for-paid-claude-plans
- https://support.claude.com/en/articles/12466728-troubleshoot-claude-error-messages
- https://support.claude.com/en/articles/8461763-where-can-i-access-claude

### Cowork
- https://support.claude.com/en/articles/13345190-get-started-with-claude-cowork
- https://claude.com/product/cowork
- https://claude.com/docs/cowork/overview (y overview.md)
- https://claude.com/docs/cowork/changelog
- https://claude.com/docs/cowork/guide/projects
- https://claude.com/docs/cowork/guide/dispatch
- https://claude.com/docs/cowork/guide/plugins
- https://claude.com/docs/cowork/monitoring
- https://support.claude.com/en/articles/14479288-claude-cowork-architecture-overview
- https://support.claude.com/en/articles/13364135-use-claude-cowork-safely
- https://support.claude.com/en/articles/15520349-use-claude-cowork-on-web-desktop-and-mobile
- https://support.claude.com/en/articles/13947068-assign-tasks-from-anywhere-in-claude-cowork
- https://support.claude.com/en/articles/13854387-schedule-recurring-tasks-in-claude-cowork
- https://support.claude.com/en/articles/14128542-let-claude-use-your-computer-in-cowork
- https://support.claude.com/en/articles/14729249-use-live-artifacts-in-claude-cowork
- https://support.claude.com/en/articles/12622703-deploy-claude-desktop-for-windows
- https://claude.com/docs/third-party/claude-desktop/local-access
- https://claude.com/docs/third-party/claude-desktop/extensions

### Skills y plugins
- https://claude.com/docs/skills/overview
- https://claude.com/docs/skills/how-to
- https://support.claude.com/en/articles/12512176-what-are-skills
- https://support.claude.com/en/articles/12512180-use-skills-in-claude
- https://support.claude.com/en/articles/12512198-how-to-create-custom-skills
- https://platform.claude.com/docs/en/build-with-claude/skills-guide
- https://code.claude.com/docs/en/skills
- https://code.claude.com/docs/en/plugins-reference
- https://code.claude.com/docs/en/discover-plugins
- https://code.claude.com/docs/en/plugin-marketplaces
- https://claude.com/docs/plugins/overview
- https://claude.com/docs/plugins/submit
- https://claude.com/plugins-for/cowork
- https://claude.com/plugins/legal
- https://support.claude.com/en/articles/13837440-use-plugins-in-claude
- https://support.claude.com/en/articles/13837433-manage-plugins-for-your-organization

### Herramientas y capacidades transversales
- https://support.claude.com/en/articles/12111783-create-and-edit-files-with-claude
- https://support.claude.com/en/articles/8241126-upload-files-to-claude
- https://support.claude.com/en/articles/9487310-what-are-artifacts-and-how-do-i-use-them
- https://support.claude.com/en/articles/9547008-publish-and-share-artifacts
- https://support.claude.com/en/articles/10593882-share-and-unshare-chats
- https://support.claude.com/en/articles/9517075-what-are-projects
- https://support.claude.com/en/articles/9519177-how-can-i-create-and-manage-projects
- https://support.claude.com/en/articles/9519189-manage-project-visibility-and-sharing
- https://support.claude.com/en/articles/11817273-use-claude-s-chat-search-and-memory-to-build-on-previous-context
- https://support.claude.com/en/articles/12123587-import-and-export-your-memory-from-claude
- https://support.claude.com/en/articles/9450526-export-your-claude-data
- https://support.claude.com/en/articles/10684626-enable-and-use-web-search
- https://support.claude.com/en/articles/11088861-use-research-on-claude
- https://support.claude.com/en/articles/10065434-use-dictation-on-claude-mobile
- https://support.claude.com/en/articles/11101966-use-voice-mode
- https://support.claude.com/en/articles/10769299-how-to-use-claude-in-your-preferred-language
- https://support.claude.com/en/articles/8664678-change-the-model-effort-and-thinking-settings
- https://support.claude.com/en/articles/10065433-install-claude-desktop
- https://support.claude.com/en/articles/11145838-use-claude-code-with-your-pro-or-max-plan
- https://support.claude.com/en/articles/12012173-get-started-with-claude-in-chrome
- https://platform.claude.com/docs/en/build-with-claude/pdf-support
- https://platform.claude.com/docs/en/build-with-claude/vision
- https://platform.claude.com/docs/en/build-with-claude/citations

### Conectores
- https://support.claude.com/en/articles/11176164-use-connectors-to-extend-claude-s-capabilities
- https://support.claude.com/en/articles/11175166-get-started-with-custom-connectors-using-remote-mcp
- https://support.claude.com/en/articles/10949351-getting-started-with-local-mcp-servers-on-claude-desktop
- https://support.claude.com/en/articles/11725091-when-to-use-desktop-and-web-connectors
- https://support.claude.com/en/articles/10166901-use-google-workspace-connectors
- https://support.claude.com/en/articles/12542951-set-up-the-microsoft-365-connector
- https://claude.com/docs/connectors/overview
- https://claude.com/docs/connectors/getting-started.md
- https://claude.com/docs/connectors/directory
- https://claude.com/docs/connectors/custom/remote-mcp.md
- https://claude.com/docs/connectors/custom/desktop-extensions (y .md)
- https://claude.com/docs/connectors/google/drive (y .md)
- https://claude.com/docs/connectors/google/gmail (y .md)
- https://claude.com/docs/connectors/google/calendar (y .md)
- https://claude.com/docs/connectors/slack
- https://claude.com/docs/connectors/building/mcp-apps/getting-started
- https://claude.com/docs/claude-tag/admins/connections/google

### Ofimática y almacenamiento (terceros)
- https://claude.com/docs/office-agents/word
- https://claude.com/docs/office-agents/dictation
- https://claude.com/docs/office-agents/connectors-and-skills
- https://support.google.com/drive/answer/13401938?hl=en
- https://support.google.com/drive/answer/6374270
- https://support.microsoft.com/en-us/office/sync-files-with-onedrive-in-windows-615391c4-2bd3-4aae-a42a-858262e42a49
- https://support.microsoft.com/en-us/onedrive/microsoft-storage-quotas
- https://support.microsoft.com/en-us/office/what-s-the-difference-between-a-paid-microsoft-365-subscription-and-the-free-web-apps-7c813f33-d3bf-4e5b-9b92-dcab8ae910d2
- https://learn.microsoft.com/en-us/office/dev/add-ins/concepts/requirements-for-running-office-add-ins

### Programas de acceso gratuito o con descuento (ninguno aplicable)
- https://www.anthropic.com/news/claude-for-teachers
- https://www.anthropic.com/news/claude-for-nonprofits
- https://claude.com/contact-sales/claude-for-oss

### URLs consultadas que devolvieron 404
- https://support.claude.com/en/articles/14680753-extend-claude-cowork-with-third-party-platforms
- https://claude.com/docs/cowork/guide/skills.md
