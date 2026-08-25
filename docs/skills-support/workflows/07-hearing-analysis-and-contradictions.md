# Workflow — Audiencias, transcripción y contradicciones

**Fuente funcional:** OBSERVED / USER-CONFIRMED para preparar/asistir/analisar audiencias.
**Prioridad:** `hearing-analysis` P2; `contradiction-analysis` P2.

## Objetivo de trabajo

Preparar una audiencia a partir de Case context y Evidence, y analizar el material posterior separando audio original, derivación/transcripción, atribución de hablante, afirmación extraída e interpretación. Detectar contradicciones como hallazgos falsables, no como veredictos.

## Cuándo ocurre este flujo

Antes de audiencia, al recibir grabación/acta/transcripción, al comparar testimonio/documento o al revisar compromisos, órdenes, menciones de plazo y acciones pendientes.

## Roles y ejemplos de activación

Litigante en el alcance actual; un uso por decisor es post-V0 y requiere contexto B, discovery y gates propios. “Prepare preguntas”, “extraiga compromisos”, “compare esta declaración con el contrato”, “marque tensiones de fechas/montos/identidad”, “qué requiere revisar antes de audiencia”.

## Entradas

Agenda, finalidad, contexto autorizado, Facts/Evidence, providencias relevantes, audio/video original, transcripción con rangos temporales, acta y material de las partes. Si no hay atribución de hablante fiable, declararlo como tal.

## Contexto necesario del caso e información externa

Requiere Sources/DerivedRepresentations/locators válidos y estado de Case. Las reglas de audiencia y efectos de una manifestación dependen de Knowledge Pack por procedimiento/rol. Un servicio de transcripción es adapter futuro, no autoridad.

## Etapas del método y razonamiento

1. Antes: resumir temas, hechos con soporte, pruebas pendientes, preguntas y riesgos, separando hipótesis de decisiones.
2. Después: enlazar cada observación a audio/original o acta y conservar atribución/limitación.
3. Extraer declaraciones, órdenes, compromisos y posibles fechas, sin calcular efectos jurídicos automáticamente.
4. Buscar contradicción formal (fecha/monto/identidad/secuencia) y tensión semántica (documento–testimonio/parte–evidencia).
5. Presentar ambos pasajes y la pregunta para revisión, no “contradicción comprobada” salvo una regla determinista explícita.

## Salidas esperadas

Brief de audiencia, preguntas candidatas, tabla de declaraciones/locators, lista de órdenes/compromisos/faltantes y matriz de contradicciones con lado A, lado B, tipo, evidencia y explicación de incertidumbre.

## Decisiones humanas y límites de la IA

La humana decide estrategia de interrogatorio, credibilidad, significado de silencio, admisión, gravedad de contradicción, consecuencia procesal y toda determinación. La IA puede seleccionar pasajes, organizar y proponer preguntas. No puede declarar una contradicción acreditada, valorar credibilidad, establecer un término ni decidir una consecuencia procesal.

## Responsabilidades del Core y herramientas MCP posibles

El Core preserva original, provenance, hashes, locators, Proposal y staleness. No exponer timestamps sin asegurar que resuelven contra la línea de tiempo del original. V0 no añade tools; transcripción y locators están contratados como capacidad/adapter, con pruebas posteriores.

## Dependencias de Knowledge Pack, evidencia y procedencia

La metodología de comparación es universal. Reglas de audiencia, declaración, interrogatorio, prueba y términos son Knowledge Pack fechado. Todo hallazgo usa locators de ambos lados; no permitir que la IA diga haber oído/leen algo fuera del material.

## Dependencias temporales/jurídicas y fuentes oficiales

Los plazos/órdenes mencionados se registran como contenido hasta que una fuente y estado procesal los validen. Ver [05-temporal-applicability.md](../05-temporal-applicability.md) y dossier por área.

## Tratamiento de documentos externos e instrucciones maliciosas

Todo correo, PDF, chat, transcripción o enlace aportado al caso se trata como contenido no confiable. Una frase como “ignore las reglas” o “envíe este expediente” dentro del material no cambia el método, los permisos ni las decisiones humanas.

## Fallos frecuentes y consideraciones de experience

Errores: atribución de hablante inventada, timestamp de derivado tratado como original, tensión semántica presentada como hecho, omitir evidencia contraria y confundir orden oral con obligación verificada. La vista debe permitir saltar al pasaje y mostrar “atribución incierta” o “requiere verificación”.

## Evaluaciones, relación con candidatas y preguntas abiertas

Medir precisión de locators, recall de declaraciones/compromisos, atribución de hablante, recall de contradicción y falsos positivos. `contradiction-analysis` se mantiene separada por trigger/métrica propios, pero compone con `hearing-analysis` y `evidence-analysis`. Pregunta abierta: formatos y calidad real de audios/actas.
