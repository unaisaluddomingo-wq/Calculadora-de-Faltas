# GUIA PARA MI PROYECTO DE CONTADOR DE FALTAS DE ASISTENCIA

## NORMAS DEL CICLO:
- Solo puedes faltar un porcentaje de las horas de cada asignatura. Ese porcentaje lo elige el usuario la primera vez
que inicia el programa (en mi centro es un 20%) y se guarda en la base de datos (tabla config), para que cualquiera
pueda usar el proyecto con las normas de su centro
- Cada asignatura tiene un total de horas (por ejemplo 33, 66, 99 o 132). Las asignaturas y sus horas las define el
usuario y se guardan en la base de datos (tabla asignaturas); asignaturas.py solo las lee
- Con un 20%, puedes faltar 20 horas en una asignatura de 132 horas y que no pase nada, y faltar ese mismo numero de horas
a una asignatura de 33, y suspenderla
- Superar ese porcentaje de faltas de asistencia supone el suspenso inmediato de la asignatura
- Las horas son de todo el año escolar, no trimestral o mensual, son de un año escolar

## NORMAS DEL PROGRAMA
- Este programa esta totalmente hecho por mi, Unai, excepto cuando se necesite llamar a la base de datos
- El codigo relacionado a la base de datos esta desarollado por Claude
- Por cada accion que puede hacer el usuario o el programa hay un script que es donde esta el codigo que realiza
esta accion, con tal de tener un codigo mas ordenado
- El programa se lanza usando main.py, que primero chequeara si existe la base de datos y si no existe la creara
- Despues de comprobarlo, main.py llamara a menu.py, que es donde interactua el usuario, y se correra en bucle
hasta el cierre del programa
- Si no existiera la base de datos se crearia automaticamente. Todo esto lo hace el archivo db_check.py
- El archivo db_check.py sirve para conectar la base de datos o en su defecto crearla, pero cada accion que
requiera usar la base de datos debe llamarse desde el propio fichero de la funcion
- Cuando se muestren todas las asignaturas, se deben mostrar de 5 en 5, y si el usuario precisa escoger otra
asignatura que no se ve, deberia poder ver las otras 5 mediante las flechas de direccion
- Cuando se muestren todas las asignaturas, se han de presentar con un numero y un punto delante, seguido de un especio
y el nombre de la asignatura. 
- La carpeta acciones solo contiene las funciones propias del programa (añadir, consultar, modificar, materias, porcentaje, sugerencia) y db_check.py.
No se crean scripts auxiliares sueltos (como pedir_fecha o elegir_asignatura): cada funcion hace por si misma
todo lo que necesita (pedir la fecha, elegir la asignatura, dibujar tablas...), con funciones privadas dentro de
su propio fichero
- Cuando se muestre cualquier lista (asignaturas, faltas...), se debe mostrar como una tabla en arte ASCII, separando
filas y columnas con los simbolos "+" y "-" (y "|" para los lados), como el cliente de MySQL en CLI
- Despues de finalizar cualquier accion como añadir, consultar o modificar faltas, se le pedira al usuario que pulse
enter para continuar
- Cuando se muestren las faltas almacenadas en la base de datos, se deben mostrar de 5 en 5. En caso de no caber,
el usuario deberia poder ver otras 5 usando las flechas de direccion
- Cuando se usen las flechas de direccion, es porque el usuario ha de elegir o una falta para modificarla o una
asignatura. Cada vez que se use la flecha para mostrar opciones, se deben borrar inmediatamente las mostradas
anteriormente
- Cuando se muestren las faltas almacenadas en la base de datos, se debe mostrar el id, la asignatura, y si es
justificada o no (S/N). Ademas se muestran la fecha y las horas para identificar mejor cada falta.
- En Python, cuando hayas de usar format, escribe siempre {} y al final .format(variable)
- Si modifico este archivo, NORMAS.MD, informare a Claude sobre ello y debera introducir las nuevas normas en 
CLAUDE.md
- Antes de aplicar cualquier cambio en este claude.md, analiza si las nuevas normas contradicen las existentes
o rompen la lógica del sistema
- Cuando se haga un commit en git, debe añadirse con la instruccion -m todos los cambios que se han hecho de 
manera general

### Funcion añadir
-   Esta funcion sirve para que el usuario pueda añadir faltas de asistencia a la base de datos. 
- La base de datos necesita saber el id (cada falta incrementa ese numero en 1), sirve para llevar el control
de todas las faltas en general, pero cada asignatura tiene que llevar su propio conteo de faltas. 
- Por ejemplo: puedes tener 5 faltas de una asignatura X, y en id puede poner 10. 
- La base de datos tambien nececita saber la asignatura a la que has faltado, la fecha, si la falta es justificada
o no, y el total de horas que el usuario ha faltado (porque hay materias que se imparten varias horas seguidas)

### Inicio del programa y funcion materias (acciones/materias.py)
- Antes de nada, si no esta establecido, se pregunta al usuario que porcentaje de horas puede faltar por modulo (1-100)
y se guarda en la base de datos (acciones/porcentaje.py). Despues se comprueban las asignaturas y se muestra la nota de
sugerencia (acciones/sugerencia.py), y solo entonces se pasa al menu principal
- Al iniciar, si la base de datos no tiene ninguna asignatura, se obliga al usuario a añadir al menos una: primero
se pregunta el nombre y luego las horas. Tras añadir la primera se le pregunta si quiere añadir mas o pasar al
programa. Si ya hay asignaturas, el programa arranca con normalidad
- La opcion "Gestionar asignaturas" del menu permite crear asignaturas, eliminarlas, cambiar su nombre o cambiar sus horas
- Los nombres no pueden estar vacios ni repetirse. Cambiar el nombre actualiza tambien las faltas de esa asignatura
- Eliminar una asignatura pide confirmacion y borra tambien sus faltas. No se puede eliminar la ultima asignatura

### Funcion consultar
- Esta funcion sirve para consultar las faltas que el usuario lleva en el curso
- Primero se le pregunta al usuario si quiere ver las faltas que lleva en total (total horas faltadas / total horas
lectivas) o si quiere ver la de alguna asignatura concreta
- Si quiere ver el total se le mostrara en formato (X/Y)
- Si quiere ver las faltas que lleva en alguna asignatura se le mostraran en formato (total faltas asignatura
especifica / total horas asignatura especifica)

### Funcion modificar
- Esta funcion le pide al usuario que elija una falta de asistencia ya registrada para modificarla o borrarla
- La funcion primero le pedira al usuario que elija la falta de asistencia sobre la que desea trabajar
- Al elejir una falta, se le preguntara al usuario si desea borrarla o modificarla
- Si desea borrarla, se le volvera a preguntar para confirmar, y si confirma se borrara de la base de datos
definitivamente, y si dice que no simplemente no se hace nada
- Si desea modificarla, se le preguntara que parametro desea modificar (todo es modificable menos el id)
- Cuando elija que desea modificar, se le pedira el valor nuevo, y se sustituira en la base de datos

### Funciones por añadir
- Si esta vacio es que no hay funciones por añadir
#### Funcion nuevo año
- El usuario podra elegir en el menu que ha empezado un nuevo año escolar, permitiendole borrar todas sus
faltas de asistencia y preguntandole sobre los nuevos porcentajes y normas de asistencia