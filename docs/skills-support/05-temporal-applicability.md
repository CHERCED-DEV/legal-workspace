# 05 — Aplicabilidad temporal y régimen jurídico

**Principio:** "vigente hoy" no responde por sí solo qué regla aplica a un Case.
**Estado de la regla:** metodología universal; los ejemplos colombianos se mantienen fechados en el catálogo.

## 1. Datos que una pregunta jurídica debe pedir

| Campo | Pregunta que responde |
|---|---|
| `jurisdiction` | ¿Qué orden jurídico/procedimiento gobierna? |
| `published_at` | ¿Cuándo fue publicada/expedida la fuente? |
| `effective_from` / `effective_to` | ¿Cuándo produce/dejó de producir efectos según fuente? |
| `repealed_at` | ¿Cuándo perdió vigencia total o parcialmente, si la fuente lo indica? |
| `transition_rule` | ¿Qué ocurre con procesos o hechos iniciados antes del cambio? |
| `case_relevant_date` | ¿Qué fecha del caso importa: hecho, presentación, inicio del proceso, decisión u otra? |
| `procedural_start_date` | ¿Cuándo se inició la actuación o proceso que puede activar un régimen transitorio? |
| `event_date` | ¿Cuándo ocurrió el hecho, conducta, pago, comunicación o evento material? |
| `decision_date` | ¿Cuándo se emitió el acto, providencia o decisión que se analiza? |
| `checked_at` | ¿Cuándo se volvió a comprobar esta información? |
| `status` | ¿Está verificada, en conflicto, desactualizada o pendiente? |

## 2. Método obligatorio

1. No empezar por la norma "actual". Empezar por el evento jurídicamente relevante y su fecha.
2. Identificar la regla de entrada en vigencia y cualquier régimen transitorio.
3. Comparar las fechas del caso contra ese régimen, declarando datos faltantes.
4. Recuperar el texto oficial aplicable y registrar su versión/consulta.
5. Si el resultado depende de interpretación, presentar alternativas y pedir revisión humana.
6. Buscar si una norma especial, por sujeto, materia, procedimiento o territorio desplaza la regla general; documentar fuente, alcance y base temporal.

## 3. Fixture de calidad: procesos laborales colombianos

La investigación debe comprobar de nuevo la Ley 2452 de 2025 y su régimen temporal antes de usarlo. La fuente oficial/repository y los valores verificados se registran en [source-catalog/temporal-law-matrix.md](source-catalog/temporal-law-matrix.md). Mientras no se confirme la fecha de inicio y el artículo transitorio contra fuente primaria, ninguna Skill puede afirmar qué código procesal gobierna un expediente laboral.

El fixture [evals/temporal-regime-labor.md](evals/temporal-regime-labor.md) exige que dos casos con hechos parecidos pero fechas procesales distintas no reciban automáticamente la misma respuesta.

## 4. Fallos que esta matriz debe detectar

- Aplicar una reforma posterior a un hecho/proceso sin examinar transición.
- Citar una versión consolidada sin saber qué redacción regía en la fecha relevante.
- Confundir fecha de publicación, expedición, promulgación y entrada en vigencia.
- Declarar caducidad, término o recurso disponible sin estado procesal procedente de registro oficial verificable, regla fechada y revisión humana.
- Ocultar que falta la fecha que decide el régimen.

## 5. Límite de la metodología

Esta metodología no resuelve retroactividad, ultractividad, favorabilidad, transición o interpretación judicial. Fuerza a identificarlas y a no inventar una respuesta. La determinación jurídica sigue siendo humana, apoyada por fuentes verificadas.
