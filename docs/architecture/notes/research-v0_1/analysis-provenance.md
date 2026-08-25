## Hallazgos

1. **SÓLIDO — Original como fuente primaria, transcripción como derivado (§6, §19).** El principio está bien formulado y es el correcto para un dominio probatorio: el derivado nunca sustituye silenciosamente al original. Es además implementable con mecanismos conocidos (almacenamiento inmutable + referencias tipadas).

2. **SÓLIDO — Dos cadenas de trazabilidad distintas (§16).** Separar la cadena probatoria (conclusión→evidencia→original) de la cadena de fuentes jurídicas (argumento→fuente→verificación) es acertado: tienen ciclos de vida, autoridades de validación y modos de fallo diferentes. No deben unificarse en un solo modelo de "cita".

3. **REFINAR — La cadena de §16 está dibujada como lineal, pero el propio documento exige un grafo.** §5.1 declara relaciones N:M entre hechos y pruebas; una conclusión puede apoyarse en varias hipótesis y una evidencia sostener varios hechos. El modelo real es un DAG de nodos tipados con aristas tipadas (soporta / contradice / deriva-de / supersede), no una cadena. Si se implementa como cadena, la primera contradicción probatoria rompe el modelo.

4. **REFINAR — §19 menciona "hash" como atributo pero no define su rol.** No es lo mismo hash-como-integridad (detectar corrupción) que hash-como-identidad (content-addressing, deduplicación de un mismo original presente en varios casos). La elección afecta ingestión, almacenamiento y el aislamiento entre expedientes (§3, riesgo 7: mezclar expedientes).

5. **RIESGO — "Verificada" no está definida (§16).** El documento solo dice qué NO basta (que el modelo la genere). Sin definir quién marca, con qué evidencia, y qué niveles existen, el flag `verificada` se vuelve decorativo y produce exactamente la falsa confianza que §28 prohíbe. Distinguir mínimo dos niveles: verificación de existencia/recuperación vs. verificación de pertinencia interpretativa (solo humana).

6. **RIESGO — El documento no aborda el anclaje de fragmentos sobre derivados regenerables.** §16 termina en "fragmento/página/timestamp" pero §19 admite que los derivados se regeneran (nuevo OCR, nueva transcripción). Offsets ingenuos sobre un derivado quedan huérfanos al regenerarlo. Sin un esquema de anclas versionadas, toda la provenance construida sobre transcripciones se invalida con cada mejora del pipeline.

7. **RIESGO — Tensión no tratada entre append-only y obligaciones de supresión de datos.** Un expediente contiene datos personales sensibles de terceros. POR VERIFICAR: alcance de las obligaciones de supresión/rectificación bajo la normativa colombiana de protección de datos (régimen de habeas data; la Ley 1581 de 2012 es el referente conocido, pero su aplicación concreta a archivos de un despacho y a expedientes de autoridad debe verificarse con la abogada/asesoría). "Append-only" absoluto puede ser jurídicamente inviable; hay que diseñar la vía de excepción (p. ej. crypto-shredding o expurgo registrado) desde el inicio, no como parche.

8. **RIESGO — Cadena de custodia previa a la ingestión (§6).** El hash en ingestión prueba integridad *desde* la ingestión, no autenticidad de la grabación ni que sea la única versión. El sistema no debe presentar "original preservado" como si acreditara autenticidad probatoria; la UX debe distinguir "no ha cambiado desde que lo incorporaste" de "es auténtico".

9. **PREMATURO — Diarización ("separar intervinientes", §6) tratada como dato.** La atribución de hablante es una inferencia del modelo con tasa de error relevante; si entra a la cadena de provenance como hecho, contamina todo lo derivado ("X declaró que…"). Debe modelarse como inferencia con incertidumbre y validación humana, y en v1 probablemente diferirse. POR VERIFICAR: qué diarización y timestamps entrega realmente el proveedor de transcripción elegido.

10. **REFINAR — Artifact Registry (§17) referencia inputs por nombre de archivo (`interview.mp3`).** Los nombres no son identidad. Los inputs deben referenciarse por (ID de entidad + hash de contenido de la versión usada); si no, la detección de "¿cambiaron los inputs?" (propiedad 9–10 del slice, §34) es indecidible.

11. **REFINAR — `audit.log` como archivo plano dentro de la carpeta mutable del caso (§13).** Un archivo de texto junto al workspace mutable es trivialmente editable y no ofrece evidencia de manipulación. Si la auditoría es un objetivo (§25, §27), necesita al menos numeración secuencial + encadenamiento de hashes, y vivir bajo el control del Core, no del filesystem del usuario.

## Respuestas

### 9. Cadena de provenance conceptual: de una frase final al fragmento original

Modelo de cinco eslabones, todos entidades con ID:

```
ArtifactVersion (doc final, inmutable, hash)
  → SupportLink[]  (qué unidad del artifact se apoya en qué)
    → Fact / Argument / LegalCitation (nodos del grafo del caso)
      → EvidenceFragmentRef (locator versionado)
        → DerivedVersion (transcripción vN, OCR vN — hash, receta)
          → Original (blob inmutable, hash)
```

Claves de diseño:

**Unidad de anclaje en el artifact.** No anclar "frases" libremente: el drafting debe componerse citando IDs de hechos/argumentos (el patrón "hecho, prueba" de §5.1 lo facilita: los hechos de una demanda son párrafos numerados naturalmente). La frase hereda la provenance del hecho que expresa. Esto convierte un problema de alineamiento texto-a-texto (frágil, costoso) en un problema de composición (barato, verificable).

**Locators por tipo de medio** (estructura `{fuente_id, versión/hash de la fuente, selector}`):

- **PDF**: `página` obligatoria; `región` (bbox en coordenadas de página) opcional; `snippet` textual como redundancia verificable. Degradación aceptada en v1: solo página + snippet, porque POR VERIFICAR qué herramientas de extracción entregan coordenadas fiables en PDFs escaneados colombianos (calidad variable).
- **Audio/video**: rango `[t_inicio, t_fin]` **sobre la línea de tiempo del original**, nunca sobre la de un clip derivado. El timestamp es el ancla durable.
- **Texto derivado**: selector doble — offsets `[inicio, fin]` sobre una versión identificada por hash **más** ancla por cita textual (texto exacto + prefijo/sufijo de contexto). HECHO VERIFICADO: este patrón de selectores combinados (TextPositionSelector + TextQuoteSelector) está estandarizado en el W3C Web Annotation Data Model (Recomendación W3C, 2017); no hay que inventarlo.

**Caso transcripción-como-derivado.** Todo fragmento de transcripción lleva selector doble: offsets sobre la transcripción-versión-X **y** rango de timestamps sobre la grabación original. Consecuencia: aunque la transcripción se regenere o se pierda, el fragmento sigue resoluble contra el original (el timestamp sobrevive; el offset no). La UI que muestra un fragmento de transcripción debe poder reproducir el audio del rango — eso hace operativo, no retórico, el principio de §6.

**Regeneración de derivados.** Regenerar produce `DerivedVersion` nueva (nuevo hash, nuevo ID de versión); la anterior no se borra mientras existan fragmentos que la referencien. La re-anclaje de fragmentos a la nueva versión es una operación explícita: se intenta por ancla semántica (cita textual / timestamp), se registra éxito o fallo por fragmento, y un fragmento no re-anclable queda marcado "válido solo contra versión anterior" — nunca se rebinda silenciosamente. Esto responde directamente al riesgo 6 de Hallazgos.

**Cadena de fuentes jurídicas** (paralela, no mezclada):

```
Argument → LegalSourceRef (identidad canónica: tipo, órgano, identificador, fecha)
  → Citation (string de cita, formato por Knowledge Pack)
  → RetrievedContent (snapshot con hash, URL/medio, fecha de recuperación)
  → VerificationRecord (nivel, quién, cuándo, contra qué snapshot)
```

"Verificada" debe descomponerse en dos estados distintos: **(a) recuperación verificada** — el Core obtuvo contenido desde una fuente de la lista blanca de fuentes autorizadas (Client/Knowledge Pack) y guardó snapshot con hash; puede marcarse automáticamente *solo* por ese camino, jamás por salida del modelo; **(b) pertinencia verificada** — un profesional confirmó que el contenido recuperado sostiene la proposición del argumento; requiere `VerificationRecord` con autor humano. La política de §24 (`allow_unverified_authorities_in_final: false`) debe poder distinguir ambos niveles. POR VERIFICAR: qué fuentes oficiales colombianas son consultables de forma estable (candidatos plausibles cuya consultabilidad programática NO afirmo: relatorías de las altas cortes, SUIN-Juriscol, Diario Oficial); si no hay acceso programático fiable, el nivel (a) se degrada a "recuperación manual con snapshot adjuntado por el humano", y el diseño debe soportar ese modo desde v1.

### 10. Identificadores

Esquema de tres planos, sin sobrecargar un solo identificador:

1. **IDs de entidad**: opacos, estables, generados por el Core (ULID o UUIDv7 — ordenables por tiempo, generables offline, sin coordinación). Uno por Case, Evidence, Fact, Artifact, DerivedVersion, etc. Nunca derivados de nombre de archivo, ruta o contenido. Nunca reutilizados.
2. **Hashes de contenido** (SHA-256): identidad de *bytes* para originales y para cada versión de derivado y de artifact. Los originales se almacenan content-addressed: deduplica el mismo documento aportado a dos casos (la *relación* Evidence↔Case es por caso; el *blob* es único), y hace la verificación de integridad trivial. La identidad probatoria es el par `(evidence_id, content_hash)`: el ID da continuidad, el hash fija los bytes.
3. **Referencias a fragmentos**: no entidades globales autónomas sino estructuras `(source_id, source_version_hash, selector)` — ver respuesta 9. Dar a cada fragmento un ID propio solo cuando algo más necesite referenciarlo (un hecho comprometido sí; un resultado de búsqueda efímero no). Esto evita una explosión de entidades sin valor.

Regeneración de derivados → nuevos IDs de versión y nuevos hashes; los IDs de fragmento existentes **no cambian**: cambia (mediante re-anclaje explícito y registrado) la versión contra la que se resuelven, o quedan fijados a la versión antigua. Anclas semánticas (cita textual, timestamps) son el mecanismo de migración, no el identificador primario: un ancla semántica sola es ambigua ante texto repetido; un offset solo es frágil; el par es robusto.

Los `supersedes` de artifacts (§17) referencian `artifact_version_id`, formando cadena acíclica verificable.

### 11. Qué debe ser append-only

**Append-only estricto (inmutable una vez escrito):**
- **Blobs originales** y sus metadatos de ingestión (hash, origen declarado, quién, cuándo). Corrección de un error de ingestión = nuevo registro que marca el anterior como erróneo, nunca edición.
- **Audit log**: con número de secuencia y encadenamiento de hashes (cada entrada incluye hash de la anterior) para que la manipulación sea detectable — condición para que "auditability" (§27) signifique algo en un despliegue local (§25).
- **Cadena de decisiones epistémicas**: eventos de commit de hechos, marcas de acreditación, registros de verificación de fuentes, con autor (humano vs. sistema vs. modelo, §30-4). Revertir = evento nuevo de reversión.
- **Versiones de artifacts y de derivados**: cada versión es inmutable; la historia no se reescribe.

**Mutable (estado corriente):**
- Punteros "versión vigente" de artifacts y derivados; estado procesal actual; pendientes; borradores en `working/`; `memory.md` (proyección regenerable, §13); índices y embeddings (caché reconstruible); metadatos descriptivos no probatorios (etiquetas, notas de trabajo).

**Recolectable bajo condiciones:** versiones de derivados no referenciadas por ningún fragmento comprometido ni artifact (son caché reproducible vía receta). Los originales, nunca — salvo la vía de excepción legal del hallazgo 7, que debe ser una operación privilegiada, registrada en el audit log, y explícita en el modelo (expurgo con acta, no `delete`).

**Sobre costo/fricción (punto e de la misión).** Granularidad sostenible en v1: provenance **obligatoria** en (i) ingestión (sobre mínimo: hash, origen, quién, cuándo — coste casi nulo, automatizable), (ii) nivel hecho→fragmentos (es el flujo natural "hecho, prueba" de la abogada; el sistema propone, ella confirma — la fricción coincide con trabajo que ya hace), (iii) citas jurídicas en documentos finales, (iv) inputs de artifacts por id+hash (automático). Provenance **no exigible en v1**: alineamiento frase-a-frase de la prosa argumentativa, provenance de material de trabajo efímero, regiones exactas en PDF (página basta), diarización. Forzar granularidad de frase en v1 mataría el flujo (cada párrafo requeriría anotación) sin que el slice de §34 lo necesite: la propiedad 6 del slice se demuestra con la cadena hecho→fragmento→original.

## Invariantes candidatos

1. **Todo original recibe hash SHA-256 en la ingestión y sus bytes jamás cambian.** Capa: Infraestructura (almacenamiento WORM/content-addressed) + Domain (regla). Prueba: intentar sobrescribir un blob → rechazo; re-hash periódico == hash registrado.
2. **Ningún derivado existe sin referencia a (original_id, hash del original, receta, versión de herramienta).** Capa: Domain (constructor de DerivedVersion) + Application. Prueba: creación sin padre → rechazo; auditoría de huérfanos vacía.
3. **Un derivado nunca se sirve como si fuera el original**: toda entrega de contenido derivado incluye identidad y tipo del original. Capa: MCP (contrato de `get_evidence_fragment`). Prueba: inspección del schema de respuesta; test de contrato.
4. **Todo fragmento referenciado está ligado a una versión concreta (hash) de su fuente; el re-anclaje es explícito y auditado.** Capa: Domain. Prueba: regenerar un derivado y verificar que ningún fragmento cambió de resolución sin evento de re-anclaje.
5. **Ningún hecho alcanza "acreditado" sin evento de decisión con autor humano identificado.** Capa: Domain (máquina de estados) + Application (autorización). Prueba: intentar transición vía tool del MCP sin identidad humana → rechazo.
6. **Ninguna fuente jurídica alcanza "verificada" (ningún nivel) por salida del modelo; nivel (a) exige snapshot recuperado de fuente autorizada; nivel (b) exige VerificationRecord humano.** Capa: Domain + MCP (no exponer tool de marcado directo al modelo). Prueba: test de que el conjunto de tools no permite la transición; test de estado.
7. **El audit log es de solo-anexado con encadenamiento de hashes verificable de extremo a extremo.** Capa: Infraestructura. Prueba: verificación de cadena; mutar una entrada → detección.
8. **Versiones de artifacts son inmutables y `supersedes` es acíclico.** Capa: Domain. Prueba: property test de aciclicidad; intento de edición de versión → rechazo.
9. **Timestamps de fragmentos de audio/video refieren siempre a la línea de tiempo del original, nunca a la de un derivado.** Capa: Domain (tipo Locator). Prueba: test de tipos/validación; caso de clip recortado.
10. **No hay referencias colgantes**: todo `(source_id, hash)` referenciado por un fragmento comprometido es resoluble. Capa: Application (GC solo de versiones no referenciadas) + job de integridad. Prueba: chequeo de integridad referencial programado.
11. **Ningún artifact registra inputs por nombre de archivo; solo por id+hash.** Capa: Application (registro de artifacts). Prueba: validación de schema del registro.
12. **Toda supresión excepcional de contenido (expurgo legal) deja acta en el audit log con autor y motivo.** Capa: Application + Infraestructura. Prueba: ejecutar expurgo en entorno de test y verificar el acta.

## ADR candidatos

**ADR-1: Esquema de anclaje de fragmentos.** Contexto: derivados regenerables invalidan offsets. Decisión posible: selector doble (posición + cita textual) estilo W3C Web Annotation para texto; página(+región opcional) para PDF; rango de timestamps sobre original para A/V. Alternativas: solo offsets (frágil); solo anclas semánticas (ambiguas); IDs por fragmento pre-segmentado (rígido, acopla la segmentación). Consecuencias: re-anclaje explícito como operación de primera clase; algo más de complejidad en el Core. Falta: capacidades reales del proveedor de transcripción (timestamps por palabra/segmento — POR VERIFICAR) y de la extracción de PDF (coordenadas — POR VERIFICAR).

**ADR-2: Almacén de originales content-addressed.** Contexto: mismo documento en varios casos; integridad; aislamiento entre expedientes. Decisión posible: blobs por hash + tabla de relación Evidence↔Case por caso. Alternativas: copia por caso (duplica, simplifica aislamiento físico); referencias externas sin copia (frágil — cae en pregunta 28/29 del documento, fuera de mi dimensión). Consecuencias: la deduplicación cruza casos → el control de acceso debe estar en la capa de relación, no en el blob; interacción con expurgo legal. Falta: requisitos de confidencialidad entre casos/contextos A y B.

**ADR-3: Mecanismo de integridad del audit log.** Contexto: despliegue local, usuario con acceso total (§25) — inmutabilidad absoluta imposible; objetivo realista es detección. Decisión posible: log en el Core (tabla) con hash-chain + anclaje periódico del hash-cabeza fuera del equipo (si existe algún destino externo). Alternativas: archivo plano (débil); firma por entrada (coste/gestión de claves). Consecuencias: verificable pero no infalsificable localmente; honestidad sobre el límite. Falta: si existe conectividad/almacenamiento externo aceptable para anclar.

**ADR-4: Semántica de "fuente verificada" en dos niveles y quién la otorga.** Contexto: hallazgo 5. Decisión posible: recuperación-verificada (automática solo vía adapter de fuente autorizada, o manual-con-snapshot) y pertinencia-verificada (solo humano). Alternativas: un solo flag (ambiguo, peligroso); verificación siempre humana (más fricción, más segura si no hay fuentes consultables). Consecuencias: la política de §24 gana granularidad; la UX debe expresar ambos estados sin jerga (§10). Falta: consultabilidad real de fuentes oficiales colombianas — POR VERIFICAR antes de decidir el peso del nivel automático.

**ADR-5: Granularidad de provenance en artifacts para v1.** Contexto: punto (e); riesgo de matar el flujo. Decisión posible: anclaje a nivel de hecho/cita, componiendo el drafting sobre IDs de hechos. Alternativas: frase-a-frase (coste alto, valor marginal en v1); solo nivel artifact→inputs (insuficiente para §16). Consecuencias: la prosa argumentativa libre queda sin anclaje fino — aceptado y declarado. Falta: validación con la abogada de que el patrón "hechos numerados" cubre sus documentos reales en ambos contextos A y B.

**ADR-6: Política de retención vs. append-only (expurgo legal).** Contexto: hallazgo 7. Decisión posible: operación de expurgo privilegiada con acta; evaluar crypto-shredding. Alternativas: ignorar (riesgo legal); retención con cifrado por-original y destrucción de clave. Consecuencias: complejidad de gestión de claves si se elige crypto-shredding. Falta: obligaciones legales concretas — POR VERIFICAR con asesoría.

## Decisiones bloqueantes

Antes del vertical slice (§34, propiedades 2, 3, 4, 6, 10):

1. **ADR-1 (anclaje de fragmentos)** — bloquea las propiedades 4 y 6: sin esquema de locator no se puede demostrar provenance ni sobrevivir una regeneración de derivado, que el slice debería ejercitar al menos una vez.
2. **ADR-2 (identidad: IDs opacos + content-addressing sí/no)** — bloquea la propiedad 2 y 3: el sobre de ingestión y el layout de almacenamiento dependen de esto; cambiarlo después migra todo.
3. **Sobre mínimo de ingestión** (qué metadatos de origen son obligatorios: hash, origen declarado, quién, cuándo) — bloquea "ingestión segura"; es barato decidirlo ahora y carísimo retro-poblarlo.
4. **Mecanismo de append-only para originales y audit log (ADR-3 al menos en versión mínima)** — bloquea "preservación de original": si el slice guarda originales en una carpeta editable sin detección, la propiedad 3 es teatro.
5. **ADR-5 (granularidad hecho-nivel)** — bloquea el diseño de `propose_facts`/`commit_reviewed_fact` y del artifact del slice; decidir frase-nivel después de construir hecho-nivel es aditivo, al revés no.

**No bloquean el slice:** ADR-4 (el slice no incluye investigación jurídica), diarización, coordenadas de región en PDF, ADR-6 (debe decidirse antes de producción real, no antes del slice — pero el diseño de ADR-2 debe dejarle la puerta abierta).

## Preguntas para los dueños

1. **¿Existe obligación (o expectativa del cliente) de suprimir información de un expediente — datos personales de terceros, material entregado por error?** Importa porque decide si el append-only necesita vía de expurgo y condiciona el diseño del almacén (ADR-2/ADR-6). Bloquea parcialmente: el slice puede avanzar, pero ADR-2 debe decidirse sabiendo la respuesta.
2. **¿Cómo llegan físicamente hoy las grabaciones de audiencias y los documentos (correo, WhatsApp, USB, plataforma judicial, escáner)?** Importa porque define qué puede afirmarse honestamente sobre origen en el sobre de ingestión y qué autenticidad NO puede acreditarse. Bloquea el diseño del sobre mínimo de ingestión (decisión bloqueante 3).
3. **¿Qué fuentes jurídicas consulta hoy la abogada y por qué medio (portales oficiales, suscripciones privadas, PDFs guardados)?** Importa para decidir el peso del nivel automático de verificación (ADR-4) y qué adapters diseñar. No bloquea el slice; bloquea la fase de investigación jurídica.
4. **En el contexto B (autoridad), ¿los documentos y grabaciones producidos deben cumplir requisitos formales de expediente (foliado, actas, formatos oficiales) que el sistema deba reflejar en la provenance?** Importa porque la trazabilidad de una autoridad puede tener requisitos normativos, no solo epistemológicos — NO TENEMOS INFORMACIÓN SUFICIENTE sobre el tipo de procedimiento. Puede esperar al slice, bloquea el diseño del contexto B.
5. **¿Quiénes además de la abogada tocarán el sistema (auxiliares, judicantes) y pueden ellos marcar hechos como acreditados o fuentes como verificadas?** Importa porque los registros de decisión llevan autor y el modelo de permisos (§30-20) depende de si hay más de un rol humano real. Puede esperar para el slice mono-usuario; bloquea el modelo de permisos definitivo.