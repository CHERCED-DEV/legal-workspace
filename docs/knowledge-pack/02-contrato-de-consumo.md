# El contrato de consumo, la cobertura declarada y la caducidad

**Fecha: 2026-08-27. Material de trabajo, no una Skill.** Es la mitad que hace útil a la otra: [01-ficha-y-verificacion.md](01-ficha-y-verificacion.md) define qué se comprueba; esto define **qué pasa cuando el sistema pide una norma**.

**No contiene una sola norma, una sola fecha ni un solo estado de vigencia.** Los ejemplos usan rellenos evidentes (`LEY-0000-0000`, `AAAA-MM-DD`).

---

## §1 — La regla dura, y la que la hace funcionar

> **R1. Sin vigencia comprobada y firmada, la norma no se sirve como citable.**

Esa sola no basta, porque deja abierta la salida por la que hoy se escapa todo:

> **R2. Una respuesta del pack distinta de `CITABLE` cierra el turno. No habilita al modelo a contestar de memoria, ni a «orientar», ni a decir lo que cree recordar.**

Sin R2, R1 es un badén: el pack calla, el modelo habla, y el resultado se lee igual de fluido que si el pack hubiera contestado. R2 es la línea más importante de los dos archivos. Es también la que cierra el canal 3 del refinado (la pregunta directa de ella, que hoy contesta el modelo desnudo).

> **R3. Toda consulta al pack lleva la fecha del caso. Sin fecha, el pack no contesta.** Una norma no es vigente o no vigente: lo es *para una fecha*. Un pack que contesta sin fecha reproduce el fallo que el corpus llama su prueba de calidad temporal — dar la misma respuesta a dos casos temporalmente distintos porque la norma está vigente hoy.

---

## §2 — El pack no almacena estados: almacena afirmaciones fechadas, y el estado se calcula al leer

Este es el mecanismo del que cuelga todo lo demás, incluida la caducidad (§6).

En la ficha no existe el valor «vigente». Existe `VIGENTE_AL AAAA-MM-DD` **firmado por una persona**. El estado que ve el sistema se calcula en el momento de la lectura, con tres datos: la ficha, la fecha del caso y el día de hoy.

```text
si  hoy > revisar_antes_de                      -> PACK_CADUCADO
si  la petición es más fina que alcance_comprobado -> FUERA_DEL_ALCANCE_COMPROBADO
si  estado_vigencia = VIGENCIA_POR_VERIFICAR
    o estado_identidad != IDENTIDAD_VERIFICADA
    o estado_vigencia = VIGENCIA_PARCIAL_AL ...  -> VIGENCIA_POR_VERIFICAR
si  fecha_del_caso < vigencia_desde
    o fecha_del_caso >= la fecha de SIN_VIGENCIA_DESDE -> FUERA_DE_LA_VIGENCIA_COMPROBADA
en otro caso                                     -> CITABLE
```

**Consecuencia buscada: si nadie mantiene el pack, el pack se apaga solo.** No hace falta que alguien lea un aviso —en el corpus hay ya tres avisos de obsolescencia y ninguno ha disparado nada—: la degradación es el resultado por defecto de no hacer nada.

---

## §3 — Las ocho respuestas

Cada respuesta tiene un código para el sistema y **una frase literal para ella**. La frase importa tanto como el código: el silencio se lee como «no hay regla», y esa lectura es el fallo que el pack existe para impedir.

| Código | Cuándo | Lo que ella lee | Qué puede hacer el sistema después |
|---|---|---|---|
| `CITABLE` | Identidad verificada, vigencia comprobada, la fecha del caso cae dentro, y la petición no es más fina que el alcance | «`LEY-0000-0000`, `art. 00` — identidad comprobada; vigente al `AAAA-MM-DD` para un caso de fecha `AAAA-MM-DD`. Comprobado por Nombre Apellido el `AAAA-MM-DD`, contra `<fuente>`. Revisar antes de `AAAA-MM-DD`.» | Citar el identificador. **No** afirmar qué dice (§4) |
| `FUERA_DE_LA_VIGENCIA_COMPROBADA` | La fecha del caso queda antes de `vigencia_desde` o dentro de `SIN_VIGENCIA_DESDE` | «Para un caso de fecha `AAAA-MM-DD`, la comprobación firmada de `LEY-0000-0000` **no la cubre**: la vigencia comprobada va de `AAAA-MM-DD` a `AAAA-MM-DD`. Qué norma regía en esa fecha es una pregunta que el pack no contesta.» | Detenerse. Es un dato positivo y valioso, no un error |
| `VIGENCIA_POR_VERIFICAR` | La ficha existe, la identidad puede estar comprobada, la vigencia no | «El pack **tiene** `LEY-0000-0000` y **no tiene comprobada su vigencia**. Eso no es lo mismo que decir que no rige, ni que sí. Nadie lo ha comprobado. Última revisión de identidad: Nombre Apellido, `AAAA-MM-DD`.» | Detenerse. Puede ofrecer abrir la ficha para que ella la verifique |
| `VIGENCIA_PARCIAL` | `VIGENCIA_PARCIAL_AL` | Lo mismo, más la `nota_de_vigencia` **transcrita literal, sin interpretar** | Detenerse |
| `PACK_CADUCADO` | `hoy > revisar_antes_de` | «Esta ficha **caducó el `AAAA-MM-DD`**. Lo que dice es lo que Nombre Apellido comprobó el `AAAA-MM-DD`, y desde entonces nadie lo ha vuelto a mirar. No se sirve como citable.» | Detenerse. La fecha de caducidad y el nombre van siempre: son lo que permite ir a pedirle una revisión |
| `FUERA_DEL_ALCANCE_COMPROBADO` | La petición es más fina que `alcance_comprobado` (se comprobó la norma, se pide un inciso) | «Se comprobó `LEY-0000-0000` a nivel de `norma completa`; usted pide `art. 00, inciso 0`. **Esa comprobación no llega hasta ahí.**» | Detenerse. Es el fallo de identidad/vigencia repetido un nivel más abajo, y aquí se hace visible |
| `NO_ESTA_EN_EL_PACK` | No hay ficha, **y la materia sí está en la cobertura declarada** | «El pack cubre esta área y **no tiene** `LEY-0000-0000`. Eso significa que nadie la ha metido ni comprobado. **No significa que no exista.**» | Detenerse |
| `FUERA_DE_COBERTURA` | No hay ficha y la materia **no** está declarada, o la fecha del caso queda fuera de la ventana declarada | «El pack **no cubre** esta área (o esta fecha). Aquí no hay información de ninguna clase: ni a favor ni en contra.» | Detenerse. Con la cobertura declarada al lado, para que ella vea de un vistazo qué sí cubre |

Etiqueta visible común a las seis últimas, ya existente en el corpus: **`NO_TENEMOS_INFORMACION_SUFICIENTE`**. El código dice *por qué*; la etiqueta dice *qué se puede hacer con eso*.

**«No encontrado no es inexistente» también dentro del pack.** La regla ya está escrita carácter a carácter en las siete skills, sobre la carpeta del caso. Aquí duele más, porque el pack es el único componente que ella no puede abrir y revisar por su cuenta: si calla, su silencio no es inspeccionable.

---

## §4 — Lo que ninguna respuesta del pack contiene

Se dice aquí porque una lista de exclusiones vale más que una advertencia genérica:

- **El texto de la norma.** El pack no lo guarda (`01` §3). Una respuesta `CITABLE` es un identificador comprobado, nunca un contenido.
- **Qué dice, qué exige o qué plazo fija.** El pack no responde «¿qué dice la ley sobre X?». Responde «¿está `LEY-0000-0000` comprobada y para qué fechas?».
- **Si aplica al caso.** Pertinencia, subsunción y estrategia son de ella.
- **Cálculo de términos.**
- **Jerarquía o especialidad entre dos normas comprobadas.** Si dos fichas responden, se entregan las dos; el pack no elige. Las reglas de precedencia entre packs siguen siendo `DECISIÓN PENDIENTE` en `architecture/boundaries.md`.

El riesgo que esto deja abierto, escrito en voz alta: **el sistema puede citar una norma que existe y que rige, y atribuirle algo que no dice.** Contra eso el pack no hace nada; lo único que lo contiene es la regla 1 del método —«el método no contiene derecho»— y que ninguna respuesta del pack sea un texto que el modelo pueda parafrasear.

---

## §5 — La cobertura declarada: el pack habla de sí mismo

Sin esto, el sistema reproduce dentro el error que persigue fuera. Se escribe una vez por versión del pack, **coste por registro cero**, y viaja en el manifiesto de `architecture/boundaries.md` §8.

```yaml
cobertura:
  materias_declaradas: [<las áreas que este pack afirma cubrir>]
  materias_excluidas:  [<las que NO cubre, nombradas una a una>]
  ventana_temporal:
    desde: AAAA-MM-DD   # antes de esta fecha el pack no dice nada
    hasta: AAAA-MM-DD   # = validity_cutoff_date
  granularidad: "por registro, en alcance_comprobado; no hay garantía uniforme"
  no_contiene: [texto normativo, interpretacion, pertinencia, calculo de terminos]

provenance:                      # exigido por boundaries.md §8
  curator: "Nombre Apellido"     # una persona, no «el equipo»
  validity_cutoff_date: AAAA-MM-DD

recuento:                        # se calcula; es el estado de salud público del pack
  registros: 00
  citables_hoy: 00
  vigencia_por_verificar: 00
  caducados_hoy: 00
```

Tres decisiones dentro de esa plantilla:

- **`materias_excluidas` se nombra una a una.** Una lista de lo que sí cubre deja el resto en penumbra; nombrar lo excluido convierte `FUERA_DE_COBERTURA` en una respuesta comprobable.
- **`validity_cutoff_date` = el `verificado_el` **más antiguo** entre los registros que el pack sirve como citables.** Un registro viejo hace pesimista la fecha de portada de todo el pack. Es el sentido correcto del error.
- **`recuento` se publica siempre.** Un pack donde 22 de 25 registros están en `VIGENCIA_POR_VERIFICAR` tiene que **verse así desde fuera**, sin abrirlo. Es la diferencia entre un pack honesto y uno que aparenta.

---

## §6 — Cómo caduca y quién lo mantiene

**Quién.** `curator` es una persona con nombre y responde por el pack. `verificado_por` es quien firmó cada registro. Cuando no coinciden, manda el segundo: la responsabilidad es por ficha, no por archivo.

**Cadencia — `PROPUESTA`, la cierran el dueño y la verificadora en P0.** Ninguna de estas cifras es un dato jurídico; son política operativa:

| Situación de la ficha | `revisar_antes_de` por defecto |
|---|---|
| Vigencia comprobada, sin nada pendiente en la nota | `verificado_el` + 12 meses |
| La nota registra un cambio con fecha futura, una entrada escalonada o un control pendiente | `verificado_el` + 3 meses, **o el día anterior a esa fecha futura si es antes** |
| `VIGENCIA_POR_VERIFICAR` | irrelevante: nunca fue citable |

**Revisión extraordinaria — la dispara cualquiera de estos, sin esperar a la cadencia:**
1. Una reforma que toca una `materia` declarada en la cobertura.
2. Una ficha cuya `nota_de_vigencia` anunciaba un cambio con fecha, y esa fecha llega.
3. Una entrada `CORRECTIVE` en el changelog de un registro relacionado.
4. **Ella reporta una discrepancia desde un caso real.** Es el disparador más barato y el único que mira al mundo en vez de al calendario. Necesita una vía de una línea para llegar al curador; si no la tiene, no existe.

**Qué pasa si nadie revisa: nada, y esa es la respuesta.** El estado se calcula al leer (§2), así que la ficha vencida deja de servirse sin que nadie actúe. Dos escalones más, por encima del registro:
- Si `recuento.caducados_hoy` supera un umbral —**`PROPUESTA`: un tercio de los citables**— el pack se declara `DEGRADADO` y lo dice en cada respuesta, incluidas las `CITABLE`.
- Si `validity_cutoff_date` queda más de **`PROPUESTA`: 18 meses** atrás sin ninguna reverificación, el pack **deja de servir `CITABLE` por completo** y solo responde identidad. Un pack sin mantenedor no debe poder seguir dando confianza en datos viejos, que es exactamente lo que se temía en §8.2.

**Changelog tipado — se reutiliza el de `boundaries.md` §8, sin inventar nada:**

| Qué cambió en una reverificación | Entrada | Efecto |
|---|---|---|
| `estado_vigencia` cambia de valor (lo anterior estaba mal o dejó de ser cierto) | `CORRECTIVE` | Invalidación fuerte: los artifacts que dependen del pack **requieren revisión**. Es el caso que este instrumento existe para hacer visible |
| Se añade un registro, o se estrecha/amplía `alcance_comprobado` | `ADDITIVE` | Aviso suave que ella decide atender |
| Cambia una URL, un rótulo o la presentación | `FORMAL` | Solo afecta al render futuro |

`POR VERIFICAR`, ya señalado en `boundaries.md` y todavía sin cerrar: un artifact producido bajo la comprobación vigente en su momento procesal puede seguir siendo correcto para ese momento. Hasta que se decida, `CORRECTIVE` avisa; no reescribe nada.

---

## §7 — Lo que este instrumento sigue sin impedir

Se escribe para que nadie lo lea como una garantía que no da:

1. **Que se cite una norma vigente atribuyéndole lo que no dice.** El pack no guarda texto (§4). Lo contiene el método, no esto.
2. **Que se cite la redacción original de un artículo reformado**, si la reforma no llegó a derogarlo y `alcance_comprobado` era la norma completa. Es el precio de haber dejado fuera `modificada_por[]` (`01` §3).
3. **Que la comprobación sea sincera pero equivocada.** El pack registra quién y cuándo, no acierta por ella. Lo que sí garantiza es que el error tiene nombre, fecha y fuente, y por tanto se puede encontrar y corregir — que es todo lo que hoy no ocurre.
4. **Que el modelo conteste igual por fuera del pack.** Lo cierra R2 (§1), y R2 es una regla escrita en las skills: hay que comprobar que se cumple con una prueba de banco que **falle** cuando una entrega contiene una cita jurídica sin respuesta `CITABLE` detrás.
5. **Que el primer pack sirva muy poco.** Va a servir muy poco. Ese es el trato que se aceptó en §8.2, y la alternativa era que sirviera mucho y a veces mal.
