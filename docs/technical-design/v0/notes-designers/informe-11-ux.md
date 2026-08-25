# Informe del disenador: 11-ux

Retorno crudo del agente que redacto este documento. Contiene: rutas, decisiones que requieren aprobacion, conflictos y POST-V0 / POR VERIFICAR.

---

(1) RUTAS ESCRITAS

- `C:/Users/HITMA/Desktop/legal-workspace/docs/technical-design/v0/11-ux-condition-catalog.md` (75 KB, 732 líneas). Único archivo creado; no se creó ningún ADR (mi encargo no tenía número asignado y ADR-007..011 pertenecen a otros agentes del workflow).

Contenido: §1 condición ≠ error ≠ mensaje de producto + contrato `Condition` (que `05` §4.1 referenciaba sin definir); §2 tres familias + justificación de `INTEGRATION_ERROR` + regla de clasificación de tres preguntas; §3 ficha completa de las 7 condiciones (family/meaning/trigger/severity/categoría/user-visible/blocking/payload/mensaje); §4 epistemología aplicada (4 pares con mecanismo estructural + mensaje INCORRECTO/CORRECTO + lexicón de techo de certeza); §5 las 4 categorías; §6 política de plantillas por locale; §7 12 invariantes + 10 tests; §8 conflictos; §9 alcance; §10 cierre anti-explosión (30→4→10); §11 referencias.

(2) DECISIONES QUE REQUIEREN APROBACIÓN (§8.5, doce)

1. Forma del contrato `Condition`, incluido `rendered` (texto ya renderizado) viajando con la condición — divergencia deliberada frente a `ToolError`, que lleva solo `message_key`. Razón: `05` §4.3 fija que el error es para el modelo y la condición para la usuaria; la condición atraviesa un canal cuya redacción no controlamos.
2. `ANALYSIS_STALE` con `blocking = false` en V0: la política "no presentarlo como vigente" del slice queda declarada **sin superficie que bloquear** (drafting es POST-V0).
3. Corrección del mensaje de `INTEGRATION_ERROR`: eliminar "puedo reintentarla cuando usted lo indique" (capacidad inexistente en las 8 tools) y añadir el efecto real: sin transcripción `READY` la grabación no entra en las búsquedas. Hereda la DECISIÓN PENDIENTE de `03` §5.
4. `policy_reason` como enum cerrado, **vacío en V0** ⇒ `OPERATION_NOT_PERMITTED` no es emisible (forma verificable de "declarada sin disparador").
5. `INTEGRATION_ERROR` clasificada `LIMITED_CERTAINTY`, no `CANNOT_DO_THAT`.
6. Regla de presupuesto de plantillas `|plantillas| ≤ |ocasiones|` y criterio de ocasión ("¿qué haría distinto la lectora?").
7. **Tratamiento por defecto de `es-CO`:** el mensaje aprobado de `HUMAN_REVIEW_REQUIRED` usa tuteo ("revises", "deseas") y toda la redacción previa del slice usa "usted". Se propone `register` como parámetro de locale; los textos aprobados se reproducen literales sin alterar.
8. Campo `coverage` en el resultado de `search_case` (toca `05` §6.3): sin él la plantilla de resultado vacío no puede declarar que hay material no indexado.
9. Unificación del formato de rango temporal con `locator_summary`: "18:42" es ambiguo entre `mm:ss` y `hh:mm` — defecto de fidelidad, no de estilo.
10. Precisión de la regla de redacción del slice: negación explícita ("nada cambió") obligatoria en ocasiones bloqueantes, suficiente por léxico en informativas (el mensaje aprobado de `HUMAN_REVIEW_REQUIRED` la sostiene por implicatura).
11. Si `NOT_INCORPORATED` merece condición propia (hueco heredado de ADR-006 / `05` §4.3).
12. Presupuesto de atención de tres condiciones por sobre.

(3) CONFLICTOS CON ADRs ACCEPTED

Ninguno. Dos tensiones registradas, ambas resueltas dentro del corpus vigente:
- Los tres textos aprobados por los dueños sustituyen redacciones que el slice declaraba `SUPUESTO`; cambia la prosa, no el código, disparador, familia ni carácter bloqueante. Hallazgo derivado: los tres cubren ocasiones distintas de las que ilustraba el slice (el `HUMAN_REVIEW_REQUIRED` aprobado es la ocasión informativa tras `propose_facts`, no la bloqueante tras commit) — evidencia empírica de que un código necesita más de una plantilla.
- Precisión de kernel §10 "el slice no tiene conectores externos" frente a `03` §5.11, que sí especifica emisión de `INTEGRATION_ERROR` ante derivación `FAILED`. Lectura adoptada: el proveedor de transcripción es un AI-capability port, no un "conector" en el sentido de kernel §15; bajo esa lectura no hay contradicción. Se pide ratificar o precisar la frase del kernel a "sin fenómeno de fallo ejercitado". La semántica del catálogo no cambia en ninguna lectura.

(4) POST-V0 / POR VERIFICAR

POST-V0: condiciones de conectores, motor de plazos y actualizaciones (entran por `INFRASTRUCTURE` sin tocar el catálogo epistémico — objeto de la separación); refinamiento de `ANALYSIS_STALE` por relevancia + DAG de artifacts; localización a otros locales; condiciones sobre entidades reservadas (`Statement` no se materializa); superficie de drafting con su gate de política; agregación/silenciamiento inteligente de condiciones repetidas.

POR VERIFICAR: (a) si el host permite mostrar salida de tools sin mediación del modelo — decide si la fidelidad de la redacción final es garantizable o solo medible; con los cinco hechos del spike de Cowork, hoy solo es medible, y así se declara (§6.4, tres mitigaciones parciales, ninguna garantía); (b) calidad de recuperación en español y calibración del umbral de `SEARCH_INCONCLUSIVE`; (c) si el proveedor de transcripción entrega scores por segmento — el fixture del benchmark no los tiene, luego `UNCERTAIN_FRAGMENT` no es disparable desde datos reales; (d) numeración `AT-xxx` frente a los `T-UX-xx` locales; (e) transporte de `conditions[]` en la capa de protocolo MCP.

Dos condiciones quedan declaradas sin disparador ejercitado en V0, en dos familias distintas: `OPERATION_NOT_PERMITTED` (`AUTHORITY`) e `INTEGRATION_ERROR` (`INFRASTRUCTURE`). Ninguna en `EPISTEMIC`.