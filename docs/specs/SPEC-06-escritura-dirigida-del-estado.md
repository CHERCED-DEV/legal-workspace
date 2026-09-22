# SPEC-06 — El archivo de estado: reemplazo dirigido, y lo suyo intocable

**Estado:** ejecutada · **Cierra:** `PM-M-8` · lo que quedaba vivo de `H-11` y del grupo `G19` · **Familia:** defecto

---

## 1. Qué problema cierra

### Lo que el backlog daba por abierto, y ya no lo estaba

`H-11` decía: *«`inventario-de-anexos` sin regla de no sobrescritura; `estado-del-caso` reescribe sin copia previa»*. **Se leyó el código el 2026-09-05 y las dos mitades están cerradas:**

| Mitad de `H-11` | Qué hay hoy en el código |
|---|---|
| `inventario-de-anexos` sin regla de no sobrescritura | **La tiene**, §1: *«Nunca sobrescribes un archivo que ya está en `2-Borradores/`… la nueva pasada sale aparte, con el número siguiente»* |
| `estado-del-caso` reescribe sin copia previa | **La tiene**, §3 Fase 6.4: copia íntegra en `2-Borradores/0-Estado del caso — anterior (AAAA-MM-DD).txt`, con la regla de ` (2)` y la orden de **no reescribir** si la copia no se pudo guardar |

Y el ítem 1.5 del plan de trabajo —*«media hora que convierte una pérdida irreversible en recuperable»*— **describe justo eso, que ya estaba hecho**. **Quinto de cinco: ningún ítem del backlog leído contra el código ha resultado estar como decía.**

### Lo que sí sigue abierto, y es otra cosa

Lo vivo del grupo es `PM-M-8`, y no es la pérdida: es **la copia**.

> **En este sistema no hay copiar y pegar.** Cada vez que un texto aparece en una salida del modelo, se **re-emite palabra por palabra**. El archivo de estado es **el único punto de todo el producto donde un texto escrito por ella vuelve a salir por esa vía**.

El método lo admite hoy, con estas palabras, en su §4:

> *«como conservarlo depende de volver a teclearlo bien, antes de cada reescritura queda una copia de la versión anterior»*

**Eso es autoatestación sobre justo lo que un modelo hace mal.** Una tilde que se cae, unas comillas españolas que se vuelven rectas, un renglón que se une con el siguiente: la copia de seguridad solo la salva **si ella lo nota**, y una normalización silenciosa no se nota. Ella abre su archivo, ve sus palabras, y no tiene motivo para ir a comparar byte a byte contra una copia.

Y hay un segundo defecto, encontrado **al escribir esta spec** y no antes: **la plantilla de §4 pone `Revisiones anteriores` por debajo de la línea `NOTAS SUYAS`**. Si lo de debajo de la marca es intocable, el histórico **no puede crecer nunca**. La marca tenía que ser el final de la parte del sistema, y no lo era.

## 2. Comportamiento observable

1. Ella escribe lo que quiera bajo `NOTAS SUYAS` y, pasada tras pasada, **le vuelve exactamente igual**: mismas tildes, mismas comillas, mismos espacios.
2. La salida dice **cuántos renglones suyos se conservaron**, y **no los transcribe**.
3. Si el archivo **no tiene** la línea `NOTAS SUYAS`, el comando **no escribe nada**: entrega el resumen en pantalla y dice por qué.
4. Si el archivo **no existe**, se dice que es la primera revisión y se crea, con el bloque de notas vacío.
5. Antes de cualquier escritura queda **la copia del anterior**, como hasta hoy. Si no se pudo copiar, no se escribe.
6. Sin Python, el comando **sigue funcionando**: reescribe solo si su bloque de notas está vacío, y si tiene algo suyo, no reescribe y lo dice.

## 3. Reglas duras

| # | Regla | De dónde sale |
|---|---|---|
| R-1 | **Lo que hay de la línea `NOTAS SUYAS` hacia abajo no vuelve a pasar por el modelo camino del disco.** Se conserva byte a byte y se comprueba después de escribir | `PM-M-8` · ADR-008 — proponer, nunca decidir |
| R-2 | **Sin la línea marcadora no se escribe.** Suponer dónde empieza lo suyo es la manera de borrarlo | `PM-M-8` |
| R-3 | **La copia previa sigue siendo obligatoria**, y sin ella no se escribe | `H-11` · Fase 6.4, que ya existía |
| R-4 | **La marca es el final de la parte del sistema.** Nada que el sistema tenga que actualizar vive por debajo de ella | Este documento — el defecto de la plantilla |
| R-5 | **Leer no es el riesgo; reescribir sí.** El método puede leer sus notas —son información del caso—; lo que no puede es volver a teclearlas | La distinción que hace ejecutable a R-1 |
| R-6 | **Si aparece texto suyo por encima de la marca, no se mueve: se le muestra y se le pregunta.** Bajarlo al bloque de notas **es re-emitirlo**, que es lo que R-1 prohíbe | Divergencia razonada con `PM-M-8` — ver §7 |
| R-7 | **El comando funciona sin Python**, peor y diciéndolo, como los otros seis programas del plugin | ADR-018 · `INSTALACION.md` |

## 4. Qué NO hace

- **No edita el contenido de sus notas.** Ni las ordena, ni las corrige, ni las traduce al formato.
- **No las imprime en pantalla.** Lo que no se imprime no se puede parafrasear.
- **No decide qué dice la cabecera.** Eso lo sigue escribiendo el método, con sus seis fases.
- **No renombra ni mueve el archivo de estado**, ni le quita el «(no editar)» del nombre.
- **No toca `1-Documentos recibidos/`**, como ninguna fase de este método.

## 5. Cómo se sabe que quedó

| # | Observable | Cómo se comprueba | Resultado |
|---|---|---|---|
| O-1 | Con notas de ella llenas de tildes, comillas españolas, guiones largos y un tabulador, tras la pasada **los bytes de la cola son idénticos** | `test_cola_identica_byte_a_byte` | **Pasa** |
| O-2 | Y la cabecera **sí cambió** —control positivo: sin él, un programa que no escriba nada pasaría O-1 con nota perfecta | `test_la_cabecera_si_cambia` | **Pasa** |
| O-3 | Con el archivo guardado por Windows en `cp1252`, la cola sigue idéntica | `test_archivo_de_windows_en_cp1252` | **Pasa** |
| O-4 | El programa **no imprime** ninguna palabra de las notas de ella | `test_no_saca_las_notas_por_pantalla` | **Pasa** |
| O-5 | Sin la línea `NOTAS SUYAS`, el archivo queda **exactamente como estaba** y no se deja copia | `test_sin_marca_no_toca_el_archivo` · `test_sin_marca_tampoco_deja_copia` | **Pasa** |
| O-6 | La copia previa es el original entero, y dos pasadas del mismo día **no se pisan** | `test_deja_copia_del_original_entero` · `test_dos_pasadas_el_mismo_dia_no_se_pisan` | **Pasa** |
| O-7 | El archivo no se crea sin pedirlo, y creado nace con el bloque de ella | `test_no_crea_sin_pedirselo` · `test_con_crear_nace_con_el_bloque_de_ella` | **Pasa** |
| O-8 | `--comprobar` mira y **no escribe ni copia** | `test_comprobar_no_escribe_ni_copia` | **Pasa** |
| O-9 | En la plantilla de §4, **`NOTAS SUYAS` es la última sección** | Se lee el `SKILL.md` | **Pasa** |
| O-10 | Una pasada real sobre una carpeta de ella | — | **Pendiente.** No lo da por pasado esta spec |

**Trece pruebas, y son capaces de fallar.** Se comprobó con dos mutantes: uno que normaliza una comilla al escribir la cola —lo que hace una re-emisión— cayó con 3 fallos; otro que reescribe entero cuando no hay marca —el defecto que esta spec cierra— cayó con 2. Un banco que no se ha visto fallar no es un banco (`PM-5.1-BANCO`).

## 6. Qué toca

| Archivo | Qué |
|---|---|
| `plugins/despacho/scripts/estado_del_caso.py` | **Nuevo.** Reemplaza la cabecera, conserva la cola byte a byte, deja la copia previa y comprueba el resultado |
| `evals/scripts/test_estado_del_caso.py` | **Nuevo.** Las trece pruebas de arriba |
| `estado-del-caso/SKILL.md` — frontmatter | `allowed-tools` para el programa |
| `estado-del-caso/SKILL.md` §1 | La regla de escritura: qué parte se reemplaza y cuál no |
| `estado-del-caso/SKILL.md` §3 Fase 0 | `--comprobar` antes de nada, y qué hacer con texto suyo por encima de la marca |
| `estado-del-caso/SKILL.md` §3 Fase 6 | Los pasos 4 y 5, con el programa y con la degradación |
| `estado-del-caso/SKILL.md` §4 | La plantilla, con `NOTAS SUYAS` de última; y las cinco reglas |
| `estado-del-caso/SKILL.md` §8 | La pregunta 9 de autoevaluación |

## 7. Qué queda fuera y por qué

- **Bajar al bloque de notas el texto suyo que aparezca por encima de la marca.** `PM-M-8` lo propone; **esta spec no lo hace, y la divergencia es deliberada**: mover ese texto es re-emitirlo token a token, que es exactamente el daño que la propuesta existe para impedir. En su lugar, R-6: se le muestra dónde está y se le pregunta. `PM-M-8` es una propuesta de un documento de planeación, no un ADR, así que apartarse de ella no exige enmienda previa (regla 2 de esta capa) — pero sí exige decirlo, y queda dicho aquí.
- **Que el programa entienda el formato de la cabecera.** No lo necesita: recibe el texto ya escrito y lo pega. Un programa que entendiera el formato sería un segundo sitio donde vive la plantilla, y **dos sitios derivan** (ADR-014, invariante 6).
- **Aplicar el mismo mecanismo a las demás salidas.** Ninguna otra tiene un bloque escrito por ella dentro. Cuando alguna lo tenga, esta es la forma.
- **Copia de seguridad de la carpeta entera** (`V-5`, ADR-013). Sigue sin existir y esta spec no la toca.
