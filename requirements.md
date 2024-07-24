# Requerimientos de la Aplicacion
Dentro del siguiente documento se explican los requerimientos para cada uno de los
modulos implementados para la aplicacion de intercalador.

## Script *Managers.py*
## Objeto Clasificacion - OC
El siguiente modulo es el encargado de manejar la separacion por atributos de la clasificacion de un libro.
### Inicializacion - I
- **I.01** - Se tienen 5 atributos principales [clase, subdecimal, temaesp, autor, anio]

- **I.02** - Se deben inicializar los atributos por defecto sin obtener un valor.

- **I.03** - El valor por defecto de los atributos es:
  - Clase, Subdecimal, Temaesp, Autor ==> A0
  - Anio ==> 1000

### GETTERS y SETTERS - GS
- **GS.01** - Se mantienen los atributos privados por lo que unicamente se cuenta con Getters para cada atributo y no se cuenta con ningun setter ya que la aplicacion se encarga de estos pasos.

### Funcion Sacar Atributos - SA
- **SA.01** - Esta funcion recibe 2 argumentos (PIPE_A y PIPE_B) ambos atributos no pueden estar vacios. Y no tiene salida ya que actualiza los atributos de la clase.

- **SA.02** - PIPE_A se separa usando el caracter '.' y PIPE_B se separa usando el caracter ' '

- **SA.03** - PIPE_A cuenta con 3 elementos maximos [clase, subdecimal, temaesp] y PIPE_B cuenta con 2 elementos maximos [autor, anio]

- **SA.04** - BUG se considera que si el autor no cuenta con un caracter alfabetico se considera que es el anio por los que se debe cambiar.
### Funcion Estandarizar - E
- **E.01** - Considera 2 modos de operacion.
  - Modo 1. con bandera True, Añade la cadena de estandarizacion (ceros) a la izquierda. EJEMPLO: BF76 --> BF000...76
  - Modo 2. con bandera False, Añade la cadena de estandarizacion (ceros) a la derecha. EJEMPLO: BF76 --> BF76000...

- **E.02** - Se considera un valor constante para estandarizar (Ejemplo 10) se toma en cuenta los caracteres del string original.
### Funcion Estandarizar Atributos - EA
- **EA.01** - Se estandariza el atributo [clase] usando el Modo 1 del requerimiento **E.01**.

- **EA.02** - Se estandariza el atributo [subtema, temaespecial, autor] usando el Modo 2 del req. **E.01**

- **MC.03** - El atributo [anio] no se estandariza
### Imprimir Modulo - IM
- **IM.01** - Se implementa una funcion para poder mostrar todos los atributos para este modulo en una cadena de texto. print(clasificacion)

## Objeto Etiqueta - E
### Inicializacion - I
- **I.01** - Un objeto de tipo Etiqueta debe contener de manera obligatoria el siguiente elemento [Clasificacion] con el siguiente formato "BG39.5.D23 .D23 1990", de manera adicional puede tener o no los siguiente elementos [Encabezado] el cual es un texto sin formato aparente {RVIZ}, [Volumen] el cual por el momento se estima un formato de tipo numerico 0-9 y [Copia] compartiendo el mismo valor numerico 0-9.

- **I.02** - Una Etiqueta debe de contar con los siguiente elementos como atributos:
  - Atributos: EL cual es un objeto de tipo clasificacion para la separacion de atributos de un clasificacion
  - Clasificacion: El cual es el argumento Clasificacion que se paso a la creacion del objeto y debe ser limpiado de cualquier tipo de basura existente en la cadena.
  - Encabezado | Volumen | Copia: Los cuales son elementos que son opcionales para la construccion de un objeto en caso de no tenerse o recibir un valor invalido se pondran los siguientes valores por default respectivamente ['', '0' y '1']
  - PIPE_A y PIPE_B = 2 cadenas dedicadas a la separacion de los pipes de clasificacion
  - Clasificacion Valida: Bandera para el estatus de la etiqueta.
  - Clasificacion Completa: Cadena que se completa utilizando todos los campos de la etiqueta. Ejemplo: RVIZU DF23.4.D23 D23 1990 V.1 C.2
### Getters y Setters - GS
- **GS.01** - Setter de Clasificacion. Esta funcion realiza un cambio de clasificacion completa. Se realizan los siguientes pasos: Limpieza de Clasificacion (Quitar caracteres no deseados), Revisar Clasificacion se revisa si la clasificacion que se agrega es valida (se puede separar) En caso de serlo se siguen con los pasos para separar los atributos y se genera una clasificacion completa.

- **GS.02** - Los setter de Volumen, Copia y Encabezado siguen el siguiente comportamiento. Si se tiene un valor valido se realizan los siguientes pasos, se obtiene el valor clave: Ejemplo de volumen V.213 --> 213 y se realiza una integracion a clasificacion completa.
### Funcion Limpiar Clasificacion - LC
- **LC.01** - Recibe un string que se entiende que es una clasificacion y se borran de la cadena los siguiente caracteres no deseados: "LX", "MAT", "V.XXXX" y "C.XXXX" dichos caracteres no deseados se reemplazan con caracteres vacios en la cadena.

### Funcion Revisar Clasificacion - RC
- **RC.01** - Busca dentro de la clasificacion buscando los siguientes separadores posibles de PIPES: usando Regex \d((\ \.)|(\.\ )|(\ )|(\.))[A-Z] donde dentro de cada parentesis se encuentra el caracter separador los cuales deben tener antes un numero y posterior a esto una Letra Mayuscula. En caso de no encontrar ningun posible separador se marca la clasificacion como incorrecta, regresando False.

- **RC.02** - Busca caracteres de espacio.punto y punto.espacio en la clasificacion y guarda la posicion donde se encuentra estos separadores. 

- **RC.03** - En caso de no encontrar los separadores de RC.02 se buscan espacios y puntos solos con la condicion especial de tener un numero y una letra mayuscula posterior. De igual manera regresa la posicion que cumple esta condicion.

- **RC.04** - Se cortan los PIPES usando la posicion de los separadores.

- **RC.05** - Se limpian ambas PIPES para quitar posibles caracteres no necesarios. En caso de PIPE A se eliminan todos los espacios. Y en el caso del PIPE B se reemplazan los puntos con espacios.

- **RC.06** - Se revisa el PIPE B en busca de letras, esto debido a que el PIPE B correcto unicamente deberia tener un grupo de letras. En caso de encontrar mas de un grupo de letras se marca la clasificacion como incorrecta.

- **RC.07** - Si pasa el proceso de filtro se actualizan todos los parametros de la etiqueta estos siendo: PIPE_A, PIPE_B y clasif usando como separador base espacio.punto " ."


### Funcion Crear Clasificacion Completa - CCC
- **CCC.01** - Junta todos los atributos necesarios para generar una clasificacion completa usnado los siguientes parametros: Encabezado, Clasificacion, Volumen y Copia.
Donde el string resultante conecta todos estos parametros

### Imprimir Modulo - IM
- **IM.01** - Imprime todos los atributos de la clase de en un solo cuadro de texto para el debugeo de la clase.

## Objeto Libro - L
### Incializacion - I
- **I.01** - Atributos de esta clase/modulo son los siguientes:
  - Titulo: titulo|Campo para ingresar el titulo completo del libro.
  - Codigo de Barras: cbarras|Codigo de barras para identificar el libro.
  - Identificacion / Indice: ID|ID entrada del libro con respecto al excel info.
  - Etiqueta: etiqueta|Clase/Modulo que contiene los datos del libro en si.
  - Estatus: estatus|Estatus del libro para identificar en la App (Valid, Error, ...)

- **I.02** - Argumentos de Inicializacion para la clase/modulo:
  - Identificacion / Indice: aID|Necesario|INT numero para identificar como indice.
  - Titulo: aTitulo|Necesario|String. Nombre del libro.
  - Codigo de Barras: aCbarras|Necesario|string. Identificador con codigo de barras QROXXXX
  - Clasificacion: aClasif|Necesario|string. clasificacion del libro. BF23.5.D23 .D23 1990
  - Volumen: aVolumen|Opcional|string. numero de volumen. V.X o X. Por defecto 0.
  - Copia: aCopia|Opcional|string. Numero de Copia. C.X o X. Por defecto 1.
  - Encabezado: aEncabezado|Opcional|string. Encabezado opcional. RVIZ. Por defecto '' Vacio.
### Getters y Setters. - GS
- **GS.01** - Todos los atributos son privados y unicamente se pueden acceder con getters y setters.
### Llenar desde Excel. - LEC
- **LEC.01** - Cargar libros usando un archivo de Excel. Se debe especificar el sufijo ".xlsx"

- **LEC.03** - Cargar archivos usando un txt como csv. Se debe especificar el sufijo ".txt"

- **LEC.04** - Al cargar un archivo txt se excluyen los elementos que no cumplen con el numero de columnas. Estos casos se deben gracias a que se cuenta con un mayor numero de separadores.

- **LEC.05** - Se consideran los siguientes encabezados dentro del archivo excel para una correcta obtencion de datos: Titulo, Codigo de Barras y Clasificacion. En caso de que no se encuentren estos encabezados se regresa el siguiente valor 'None'

- **LEC.06** - Para encontrar los 6 encabezados posibles se consideran las siguientes cadenas de texto como mas favorables dentro de un excel:
  - Titulo - Titulo con o sin acento. Regex tit|tít
  - Codigo de Barras - Bar o codi o códi con acento. Regex bar|codi|códi
  - Clasificacion - Regex clas
  - Copia - Regex cop
  - Volumen - Regex vol
  - Encabezado - Regex enca|head

- **LEC.07** - Si se pasan los filtros se pasa a la siguiente seccion que es la creacion de los objetos de tipo libro usando el constructor de inicializacion correspondiente

### Imprimir Modulo Libro. - IML
- **IML.01** - Muestra los elementos del libro dentro de una cadea de texto tipo string, hace uso de la impesion del modulo etiqueta.

## Modulo Manejo Tabla. - MT
### Inicializacion - I
- **I.01** - El Objeto Manejo Tabla no requiere nigun valor de incializacion por el momento.

- **I.02** - Los atributos que maneja este objeto son los siguientes:
  - Tabla Datos: Es la tabla que despliega la informacion que ve el usuario. La cual tiene la siguiente forma para sus elementos: [Clasificacion Completa | PIPE_A | PIPE_B | Estatus Libro]
  - Tabla Formato: Es la tabla encargada de guardar el formato de los elementos. Tiene el siguiente formato: [Numero Elemento (Libro) | Color] Esta tabla se maneja con los estatus que puede tener el libro.
  - Lista Libros: Es la lista que cuenta con todos los libros cargados a la aplicacion, esta no cuenta con ningun orden.
  - Lista Modificados: Esta lista contiene todos los libros que fueron modificados durante la sesion, por lo que solo se puede tener una instancia del libro en toda la lista.
  - Esatus Color: Es una lista con todos los posibles estatus que puede tomar un libro explicados a continuacion:
    - Libro Valido "Valid" #FFFFFF: Representa que un libro cumple con la norma del programa.
    - Libro con Error "Error" #F04150: Representa un libro con algun error en su clasificacion.
    - Libro Seleccionado "Selected" #498C8A: Representa un libro seleccionado para el usuario: Para esta implementacion no se usa este estatus.
    - Libro a Modificar "Modify" #E8871E: Representa un libro seleccionado para se modificado.
### GETTERS y SETTERS - GS
- **GS.01** - Contamos con un getter que es para obtener la longitud de los libros cargados denominado como get_table_len()

### Operaciones Generales de la Tabla.
---
### Crear Tabla - CT
- **CT.01** - Carga todos los libros a la variable lista_libros a la aplicacion haciendo uso de la funcion del Objeto Libro llenar_desde_excel() la cual utiliza una ruta de archivo.

- **CT.02** - Utiliza la funcion agregar_elemento() la cual utiliza los libros cargados para mostrarlos en las tablas de los atributos.
### Reset Tabla - RT
- **RT.01** - Reinicia todos los atributos del objeto. Reinicia todo el programa.

### Funciones de Manejo de Elementos.
---
### Agregar Elemento. - AE
- **AE.01** - Con base en el estatus se le da un color al libro y esto se guarda en el elemento formato el cual cuenta con Indice Libro | Color.

- **AE.02** - Si el libro cuenta con algun error en su Clasificacion se agrega a un diccionario secundario donde la llave sera por medio del Codigo de Barras. Esto es uando la funcion agregar_elemento_error() que usa el objeto Libro.
### Agregar Elemento Error. - AEE
- **AEE.01** - Se agrega al diccionario de errores un libro utilizando como llave el codigo de barras del libro y cargando el libro con error.
### Agregar Elemento Modificado - AEM
- **AEM.01** - se agregar al diccionario de libros modificados un libro, utilizando como llave el codigo de barrras del libro y cargando la siguiente estructura [El Libro y la Modificacion realizada]
### Actualizar Datos Elemento - ADE
- **ADE.01** - Modificar la informacion de un libro por lo que debera modificar los datos vistos por el usuario y la lista de los libros cargados.
### Actualizar Estatus Elemento - AEE
- **AEE.01** - Cambia el estatus de un libro lo cual cambia la aparencia (Color e informacion) en la pantalla que ve el usuario.
### Eliminar Elemento Error. - EEE
- **EEE.01** - Se eliminar un elemento de la tabla error, si este elemento se encuentra en la misma en caso contrario se ignora este paso.

### Operaciones Finales de la Tabla.
---
### Ordenar Libros. - OL
- **OL.01** - Para ordenar los libros con base en la clasificacion y usando los atributos se toman el siguiente orden de importancia: [Clase, Subdecimal, Tema Especial, Autor, Año, Volumen, Copia]

- **OL.02** - El programa arroja una lista con indices donde cada indice simboliza un libro y el orden en el que esta la lista es el orden que deberá de tomar el programa | excel.
### Organizar Libros Tabla. - OLT
- **OLT.01** - Se deben generar copias de las listas que se van a modificar que son las siguientes: Tabla Datos, Tabla Formato y Lista Libros.

- **OLT.02** - Se llenan estas listas siguiendo un orden que se establece en la funcion y que recibe la funcion como argumento.

- **OLT.03** - Por ultimo si todo salio bien se copian dichas listas auxiliares con las originales para finalizar el proceso.
### Organizar Libros Excel. - OLE
- **OLE.01** - Carga un dataframe de un excel usando una ruta que se da como argumento.

- **OLE.02** - Crea un dataframe ordenado, insertando las filas que se indican usando como referencia de orden la lista_libros para ubicar cada fila de manera ordenada.

- **OLE.03** - Genera Columnas personalizadas del programa con los cambios y modificaciones hechos en la misma usando el mismo orden dado por lista_libros

- **OLE.04** - Añade las columnas generadas al dataframe ordenado del excel y da como salida dicho dataframe combinado y ordenado.

- **OLE.05** - Hacer una distinción para poder cargar archivos txt con separacion csv
### Guardar Libros Tabla. - GLT
- **GLT.01** - Se debera cargar un archivo excel o csv como dataframe de datos de referencia.

- **GLT.02** - Se generan columnas adicionales con los valores trabajados dentro del programa. y usando el orden del mismo las siguientes son las columnas generadas: Copia, Volumen, Clasificación, Encabezado, Clasificación Completa, estatus.

- **GLT.03** - Se integran estas columnas generadas, cabe mencionar como nota que estas columnas generadas pueden reemplazar columnas existentes dentro del archivo final.

### Escribir Excel. - EE
- **EE.01** - Para esta funcion se requieren los siguientes elementos: Una ruta de guardado, un nombre para el archivo y un dataframe de pandas.

- **EE.02** - Utilizando la funcion ExcelWriter de pandas se realiza una escritura a un archivo si esta se cumple de manera exitosa. Se guarda el archivo.

- **EE.03** - En caso de que la escritura marque un error cachar este error con try except y repetir el proceso de escritura pero añadiendo al nombre del archivo final el sufijo "_copia"
### Creacion de Reportes sobre Tabla.
---
### Crear Reporte General - CRG
- **CRG.01** - Genera un archivo Txt con el nombre del archivo trabajado añadiendo el sufijo '_reporte' al archivo final.

- **CRG.02** - Dentro del reporte se deberan mostrar los siguientes datos:
  - Total de Libros cargados.
  - Total de Libros que pasaron el estandar, sin realizar modificaciones
  - Total de Libros que fueron modificados para antender el estandar.
  - Total de Libros que cuentan con errores y no han sido modificados.

- **CRG.03** - Se deberan generar 2 reportes adicionales en el archivo.
  - El primero despliega una lista de los libros modificados en caso de que existan. La lista tiene la siguiente forma: Titulo del Libro | Clasificacion Final | Clasificacion que fue Modificada | Codigo de Barras del Libro.
  - El segundo se trata de una lista para mostrar los libros que aun cuentan con errores en sus clasificaciones. La lista tiene la siguiente forma: Titulo del Libro | Clasificacion | Codigo de Barras del Libro.


## Script GUI.py
## Modulo Ventana General
- **MVG.00** - Los colores de la pagina son los siguientes: Color de Fondo #3016F3, Texto #000000, Entrada y color secundario #DEE6F7

- **MVG.01** - Se cuenta con una funcion llamada resource path la cual tiene la tarea de pasar todos los ASSETS a un archivo comprimido para su portabilidad/
### Layout Izquierdo. - LI
- **LI.01** Se requiere un boton para seleccionar un archivo de Excel, donde se muestre si se tiene un archivo seleccionado o no con la siguiente leyenda: 'Sin Archivo' al comenzar el programa o no terminar el proceso de cargado. 'Nombre del Archivo' al seleccionar un archivo de excel.

- **LI.02** - Se requiere un boton para cargar el archivo seleccionado de excel al programa.

- **LI.03** - Se consideran 2 opciones finales del programa, generar un reporte opcion 'Reporte' y generar un excel ordenado 'Excel Orden'

- **LI.04** - Se toma el logo del Tec de Monterrey y el nombre de la apliacion es 'INTERCALADOR'

- **LI.05** - Se tiene la opcion de nombrar el archivo de salida, este campo es obligatorio pero en caso de dejarse vacio se toma como base el archivo de excel cargado y se genera una copia del mismo.

- **LI.06** - Se podran considerar archivo tipo ".txt" a la hora de cargar un nuevo archivo
### Layout Tabla de Datos. - LTD
- **LTD.01** - Se tiene una tabla donde se incluyen todos los libros cargados al programa. La tabla cuenta con las siguientes 4 columnas:
  - Clasificacion: La clasificacion obtenida del libro.
  - PIPE_A: Seccion de la clasificacion que contiene los siguientes posibles campos: Clase, Subdecimal y TemaEsp
  - PIPE_B: Seccion de la clasificacion que contiene los siguientes posibles campos: Autor y Anio
  - Estatus Libro: Se tiene el estatus general del libro con los siguientes posibles estatus. Error | Valid | Selected | Modify
- **LTD.02** - Cada libro tiene la posibilidad haciendo seleccionarlo para poder modificar los atributos dentro del libro.

- **LTD.03** - Un boton denominado 'Ejecutar' para ejecutar todo el ordenamiento del programa.

- **LTD.04** - Un boton para reiniciar todo el programa y empezar con uno nuevo, boton 'LIMPIAR'
### Run Window. - RW
- **RW.01** - Al salir del programa si no se tiene nada en la aplicacion, se cierra la aplicacion en caso se muestra un pop up para realiza un guardado del programa con la funcion guardar_programa o no guardar el progreso. Se tiene implementado un boton para poder guardar el programa cada que sea necesario.

- **RW.02** - El programa debera poder mostrar licencias de usuario y la version que esta manejando por medio de los siguientes 

- **RW.03** - Al presionar sobre el boton con simbolo de cargar se manda llamar la funcion seleccionar_excel() para obtener la ruta de un archivo excel y actualizar la visualizacion del programa.

- **RW.04** - Al presionar el boton 'Cargar' se activa la funcion cargar_excel, con la cual se cargan los datos del excel seleccionado, al programa, actualizando la tabla principal del sistema.

- **RW.05** - Al presionar el boton 'Limpiar' se reinicia el programa por completo haciendo llamar la funcion reset_window() y regresando al objeto modify_object a su estado base.

- **RW.06** - Un elemento se puede seleccionar presionando sobre el en la tabla, este pasara por los siguientes estatus: 
  - Elementos Valido: Valid -> Modify -> Valid.
  - Elementos Erroneos: Error -> Modify -> Valid | Error.
Esto se logra con la funcion table_control(). Para seguir por estas opciones de seleccion, unicamente se puede modificar un elemento a la vez.

- **RW.07** - Se podra modificar un elemento con el estatus 'MODIFY' de la tabla haciendo click derecho y presionando en el boton y verificando que la Bandera Modify sea 'True' para hacer uso de la funcion modificar_elemento().

- **RW.08** - Al presionar el boton ejecutar se llama la funcion ejecutar_programa()

- **RW.09** - Se podra desplegar mas informacion del libro si este se encuentra en un estatus 'MODIFY', esto se logra haciendo click derecho y presionando el boton 'Información'
### Guardar programa. - GP
- **GP.01** - Se revisa si la tabla cuenta con contenido, en caso de no tenerlo se omite el guardado 'Sin datos para guardar'

- **GP.02** - Se revisa si se tiene un archivo de excel base, en caso de no tenerlo se omite el guardado 'Sin Ruta para guardar'

- **GP.03** - Se despliega un pop up (pop.save_file()) para confirmar si se desea guardar el progreso. Positivo se sigue con el programa en caso contrario se cancela el guardado 'No continuar con guardado'

- **GP.04** - Se puede saltar el paso de preguntar con una bandera de bypass en caso de ser True, por defecto esta en False.

- **GP.05** - Se realiza una copia del excel por temas de seguridad a la hora de guardar cualquier tipo de informacion de la aplicacion. Por lo que se toma el nombre de donde se tomaron los datos y se agrega el sufijo '_saved' para poder aclarar la copia. 

- **GP.06** - Se utiliza una funcion guardar_libros_tabla que genera un dataframe igual al excel original agregando las correciones hechas en el programa. 
NOTA esta funcion puede no dar los resultados esperados en el caso de que se ejecute el programa para ordenar ya que no considera el orden del excel.
NOTA esta funcion puede generar un dataset con columnas adicionales debido a posibles errores de nombres.

- **GP.07** - Se utiliza la funcion del modulo Table Manager llamada escribir_excel() para escribir el excel de salida.

- **GP.08** - Cuando se guarde una copia con el sufijo '_saved' agregar un numero como identificador adicional. ejemplo 'excel_saved1.xlsx'

- **GP.09** - En caso de tener el sufijo '_saved' en lugar de anadir un segundo sufijo '_saved' se anade un numero adicional
### Seleccionar Excel. - SE
- **SE.01** - La funcion debera abrir un explorador de archivos para seleccionar unicamente archivos de excel.

- **SE.02** - Posterior a la seleccion del archivo se guarda el nombre del archivo y en caso de que el proceso se cancele dicho nombre se mantiene como vacio.

- **SE.03** - En caso de tener un nombre de archivo actualizar el elemento EXCEL_TEXT con el nombre o en caso de no contrar con una ruta u archivo poner por defecto el texto 'Sin Archivo'
### Cargar Excel. - CE
- **CE.01** - Se revisa si se tiene un archivo para cargar en caso contrario activar el pop.warning_excel_file() para informar al usuario que debe seleccionar una archivo y teminar el proceso.

- **CE.02** - En caso de tener un archivo seleccionado mandar llamar la funcion crear_tabla() del modulo Manejo Tabla, para cargar todos los libros del archivo de excel.

- **CE.03** - Se revisa el estatus de la funcion crear_tabla() y si se da un resultado negativo 'False' se concluye que hubo un error con los encabezados. Se manda llamar un pop.error_excel_head()

- **CE.04** - Se revisan cuantos elementos se cargaron al sistema, y en caso de superar 5000 elementos se da un aviso por medio del pop.warning_excel_size()

- **CE.05** - Actualizar los valores de la tabla principal para mostrar los datos cargados, en conjunto con los colores correspondientes a sus estatus en este caso unicamente 2 estatus son posibles: 'Error':'#F04150', 'Valid':'#FFFFFF'.

- **CE.06** - Ordenar todos los elementos de la tabla usando 

- **CE.07** - Si se cuenta con datos cargados en el programa anunciar al usuario por medio del pop.warning_excel_used() que unicamente se puede cargar un archivo de excel a la vez y abortar el proceso de cargar.
### Reset Window. - RW
- **RW.01** - Se hace uso de la funcion reset_table() del modulo Manejo Tabla, la cual de manera resumida reinicia todos los valores de la tabla.

- **RW.02** - Se eliminan la ruta del archivo de excel seleccionado y el nombre designado para el archivo de salida.

- **RW.03** - Actualizar vista de la tabla a una tabla vacia.
### Table Control. - TC
- **TC.01** - Si no se selecciona ningun libro valido, la funcion termina y regresa modify_object sin modificaciones.

- **TC.02** - Se extraen los datos del libro seleccionado: INDICE En la tabla, ESTATUS que maneja el libro.

- **TC.03** - Se actualiza el estatus del libro seleccionado usando la funcion actualizar_estatus_elemento() del modulo Manejo Tabla se pueden tener los siguientes casos:
  - Libro Valido: Valid -> Modify. Se selecciona un elemento para modificar, se guarda el estatus 'Valid' y se guarda el indice del libro 'INDEX' y se actualiza la bandera modificar a 'True'.
  - Libro Error: Error -> Modify. Se selecciona un elemento para modificar, se guarda el estatus 'Error' y se guarda el indice del libro 'INDEX' y se actualiza la bandera modificar a 'True'
  - Libro Modificar: Modify -> Valid | Modify -> Error. Para deseleccionar un elemento, se regresa al estatus anterior ('Valid'|'Error') y se libera la bandera modificar a  'False'

- **TC.04** - Solo se puede modificar un libro a la vez por lo que se maneja una bandera para aceptar unicamente un elemento. La bandera tiene el siguiente comportamiento: 'False' sin libro a modificar. 'True' libro para modificar seleccionado.

- **TC.05** - Se debe actualizar los estatus de los libros en la tabla principal.
### Modificar Elemento. - ME
- **ME.01** - Se obtiene la informacion del modulo libro con todos sus datos.

- **ME.02** - Se debera guardar la clasificacion previo a la modificacion por temas de reportes.

- **ME.03** - Se despliega una ventana secundaria para modificar el libro en su totalidad.

- **ME.04** - Si el libro se modifica se regresa un objeto de tipo Libro con todas las modificaciones, en caso de que no se modifique o se cierre la ventana se regresa un objeto de tipo 'None', si sucede este caso se cancela el proceso de modificacion y se regresa un valor 'True'.

- **ME.05** - Cuando un libro se modifica, se debe agregar a una lista de libros modificados para tener un conteo de las modificaciones relacionadas usando la funcion agregar_elemento_modificado() del modulo Manejo Tabla.

- **ME.06** - Una vez que se modifica el elemento este cambio se debe ver reflejado en la tabla principal. El texto y estatus. Usando las funciones actualizar_elemento() y actualizar_estatus_elemento()

- **ME.07** - Actualizar los elementos de la tabla.

- **ME.08** - Al terminar de modificar un elemento con error se debera eliminar dicho libro de la lista de error.

- **ME.09** - Los elementos se deberan de reordenar para acomodar el nuevo libro que entra en el estandar.
### Ejecutar Programa. - EP
- **EP.01** - Se revisa si se cuenta con datos en la tabla en caso de no tenerlos el proceso de ejecucion se aborta y se muestra un mensaje en pantalla pop.warning_data().

- **EP.02** - Se revisa si se tiene algun archivo de excel seleccionado en caso de que no se tenga ninguno seleccionado se aborta el proceso y se muestra un mensaje en pantalla pop.warning_excel_file()

- **EP.03** - El programa requiere que se seleccione una opcion valida del proceso por lo que se debe seleccionar como minimo una opcion.

- **EP.04** - El programa debe desplegar una opcion para seleccionar un folder donde guardar los datos que va a generar. En caso de cancelar este proceso se cancela todo el proceso de ejecucion.

- **EP.05** - Se extrae de la ruta del archivo seleccionado de excel su nombre sin tener los caracteres '.xlsx'

- **EP.06** - Al seleccionar REPORTE, se genera un reporte general usando la funcion crear_reporte_general() para dar datos del archivo actual y de manera adicional se genera un segundo reporte el cual contiene todos los codigo de barras de los libros que hayan sido modificados o no cuenten con el estandar correcto esto con la funcion crear_report_QRO().

- **EP.07** - Al seleccionar Orden Excel se genera un excel ordenado. Donde se realizan los siguientes pasos:
  - Debido al funcionamineto del programa se entiende que antes de presionar ejecutar todos los libros de la aplicacion estan ordenados.
  - Se ordenan los libros del excel usando la funcion organizar_libros_excel() que genera un dataframe ordenado de los libros.
  - Se da un nombre final al archivo con base al nombre dado por el usuario o en caso de que no se de un nombre por el usuario se usara el nombre del archivo seleccionado agregando el sufijo '_ordenado'
  - Se genera un nuevo excel con el nombre seleccionado anteriormente.

- **EP.08** - Notificar al usuario que el proceso termino con exito y la ruta donde se encuentran los archivos generados.

## Script support_windows.py
## Modulo Ventana Modificar. - MVM
### Inicializacion - I
- **I.01** - Para su inicializacion requiere un objeto de tipo Libro, del cual obtiene los elementos. En caso de no pararse dicho objeto se iniciaria todo el programa con elementos vacios.
### Layout General. - LG
- **LG.01** - Se despliega en como enfoque principal la clasificacion completa del libro, la cual debera ser actualizada en tiempo real, pero no podra ser seleccionada por el usuario sino que debera actualizarse con las acciones y modificaciones que realiza el usuario.

- **LG.02** - Se integra una seccion donde se puedan mostrar y modificar los siguientes elementos de la clasificacion del libro:
  - Clasificacion : Donde se planea modificar la clasificacion principal.
  - Encabezado: Donde se puede agregar un encabezado al inicio de la clasificacion completa si se desea.
  - Volumen: Seccion para modificar el valor unicamente acepta valores numericos.
  - Copia: Mismo funcionamiento que la seccion de volumen.
  - PIPE A y B, ambas secciones son de debugeo utilizados para mostrar la separacion de los atributos de la clasificacion.

- **LG.03** - Un boton con forma de 'i' mediante el cual se podra desplegar el nombre del libro por medio de un pop up.

- **LG.04** - 2 Botones para terminar el proceso de modificacion:
  - Cancelar: Cancela todo el proceso y no realiza absolutamente ningun cambio al libro, esta opcion debe mostrar una bandera cuando se activa.
  - Modificar: Finaliza el proceso de modificacion cambiando la clasificacion y atributos del libro. Esta opcion unicamente se activa si se cumple con una clasificacion correcta.
### Run Window. - RW
- **RW.01** - Al cerrar la ventana o presionar el boton de 'Cancelar' se regresa un objeto nulo o 'None' para informar a otra interfaz que no se realizo ninguna modificacion

- **RW.02** - Al presionar el boton 'INFO' se despliega un pop up nombrado pop.
show_info_libro() para mostrar el titulo del libro.

- **RW.03** - Al actualizar cualquier elemento posible, se actualizan 3 secciones de la ventana: Clasificacion Completa 'CLAS_FULL', PIPE_A y PIPE_B 'PIPE_A' 'PIPE_B' y El boton Modificar que se habilita con base en el estatus del libro. Todo esto se logra con la funcion actualizar_ventana()

- **RW.04** - Al presionar el boton Modificar este cierra la ventana y regresa el libro modificado. por completo.


## Requerimiento Implementados - RI


## Requerimientos Nuevos. - RN
- **RN.01** - Modificar proceso de corte para detectar casos con . autor y anio  M1234.D23 1900 -> M123 .D23 1900
- **RN.02** - Agregar lectura de Txt separados con CSV para lectura directa de SIERRA.
- **RN.03** - Detectar Columna CLASIFICAC
- **RN.04** - Agregar al archivo de salida una columna nombrada estatus.
- **RN.05** - Clase - Ceros a la izquierda. Subdecimal - Ceros a la izquierda. Tema - Ceros a la izquierda. Autor - Ceros a la Derecha. Anio sin cambios.

## Requerimientos Planeados. - RP
- **RP.01** - Implementacion para ordenamiento con escaneo.
- **RP.02** - Implementar posible mejora Logica de LLenado D23.4.D2.D23.1900
