
Práctica realizada por:
 - Marcos López Sobrino
 - Alfonso Barragán Carmona


Intrucciones:
-------------

Antes de iniciar el programa, ejecutamos:

 ~$ sudo pkill -9 -f icegrid

 ~$ sudo service icegridregistry stop

 ~$ sudo service icegridnode stop

Ahora, para iniciarlo:

 ~$ make start-grid

 -> Se iniciarán los nodos de IceGrid, se aplicará la plantilla...

Como comando opcional se puede usar:

 ~$ make log

 -> Crea un archivo log.txt que contiene la salida del programa.

Para detener el programa:

 ~$ make stop-grid

Para detener el programa y limpiar:

 ~$ make clean
