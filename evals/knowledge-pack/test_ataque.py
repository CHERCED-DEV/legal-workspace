# -*- coding: utf-8 -*-
"""
El adversario. **Vacío, y eso es el estado bueno.**

Aquí se escribe un test por vía NUEVA, y la convención es al revés que en
todas partes: **si el test pasa, la vía está abierta**. Cada uno intenta colar
una cita falsa y tiene éxito cuando hay un agujero. Ninguno corrige nada;
todos documentan. Que este archivo esté vacío significa que ahora mismo no hay
ninguna vía demostrada, no que no las haya.

EL CICLO, que es lo único que hay que saber para usar esto:

  1. Se ataca `contrato.py` por donde la ronda anterior no miró y se escribe
     un test por cada agujero que se encuentre, **redactado para pasar**. La
     suite en verde es la lista de vías abiertas, contadas y reproducibles.
  2. Se cierran en `contrato.py`. Se arregla el código, nunca el test: si un
     ataque describe una conducta que en realidad es correcta, eso se dice y
     se razona, no se ablanda en silencio.
  3. Cada ataque cerrado se reescribe afirmando la conducta correcta y se
     **muda a `test_vias.py`** con su prefijo. Este archivo vuelve a quedar
     vacío y aquel sube.

Ese tercer paso es el que hace converger el ciclo, y se ve en un solo número:
`test_vias.py` **solo sube**. Doce vías de las dos críticas en prosa, más
cinco campos y un control positivo: 19. Dieciocho de la primera ronda
adversaria: 37. Lo que baja es lo que queda por encontrar, y eso no se puede
contar; lo que sube sí.

La primera ronda entró por cuatro sitios, y anotarlos ahorra empezar de cero:

  - **el token como credencial al portador** —quién lo emite, cuándo, contra
    qué se resuelve y qué de lo que exhibe se vuelve a leer—;
  - **el orden de las comprobaciones**, que es donde una condición correcta
    se vuelve inalcanzable y una excepción se escapa por delante de la guarda
    que la habría atrapado;
  - **los campos que la consulta trae y nadie compara con la ficha**, que se
    reconocen porque se validan al entrar y no se leen después;
  - **el borde del calendario y la lista negra**, que son la misma cosa: sitios
    donde el contrato dejó de enumerar lo que acepta.

    cd evals/knowledge-pack && python -m unittest test_ataque -v

Cuando haya algo que escribir aquí, va con las mismas fichas de ejemplo de
`fichas.py`: aquí tampoco hay derecho.
"""

import unittest

if __name__ == "__main__":
    unittest.main(verbosity=2)
