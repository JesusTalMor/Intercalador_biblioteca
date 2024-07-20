# Requerimientos de la Aplicacion
Dentro del siguiente documento se explican los requerimientos para cada uno de los
modulos implementados para la aplicacion de intercalador.

## Script *Managers.py*
### Modulo Clasificacion
---
El siguiente modulo es el encargado de manejar la separacion por atributos de la clasificacion de un libro.
#### Inicializacion
**MC.01** - Se tienen 5 atributos principales [clase, subdecimal, temaesp, autor, anio]

**MC.02** - Se deben inicializar los atributos por defecto sin obtener un valor.

**MC.03** - El valor por defecto de los atributos es:
- Clase, Subdecimal, Temaesp, Autor ==> A0
- Anio ==> 1000

#### GETTERS y SETTERS
**MC.04** - Se mantienen los atributos privados por lo que unicamente se cuenta con Getters para cada atributo.

#### Sacar_atributos
**MC.05** - Esta funcion recibe 2 argumentos (PIPE_A y PIPE_B) ambos atributos no pueden estar vacios. Y no tiene salida ya que actualiza los atributos de la clase.

**MC.06** - PIPE_A se separa usando el caracter '.' y PIPE_B se separa usando el caracter ' '

**MC.07** - PIPE_A cuenta con 3 elementos maximos [clase, subdecimal, temaesp] y PIPE_B cuenta con 2 elementos maximos [autor, anio]

**MC.08** - BUG se considera que si el autor no cuenta con un caracter alfabetico se considera que es el anio por los que se debe cambiar.
#### Estandarizar
**MC.09** - Considera 2 modos de operacion.
- Modo 1. con bandera True, Añade la cadena de estandarizacion (ceros) a la izquierda. EJEMPLO: BF76 --> BF000...76
- Modo 2. con bandera False, Añade la cadena de estandarizacion (ceros) a la derecha. EJEMPLO: BF76 --> BF76000...

**MC.10** - Se considera un valor constante para estandarizar (Ejemplo 10) se toma en cuenta los caracteres del string original.
#### Estandarizar_atributos
**MC.11** - Se estandariza los atributos [clase, subdecimal, temaesp] usando el Modo 1. del requerimiento **MC.09**.

**MC.12** - Se estandariza el atributo [autor] usando el Modo 2 del req. **MC.09**

**MC.13** - El atributo [anio] no se estandariza
#### Imprimir modulo
**MC.14** - Se implementa una funcion para poder mostrar todos los atributos para este modulo.

### Modulo Etiqueta
---
#### Inicializacion
**ME.01** - Un objeto de tipo Etiqueta debe contener de manera obligatoria el siguiente elemento [Clasificacion] con el siguiente formato "BG39.5.D23 .D23 1990", de manera adicional puede tener o no los siguiente elementos [Encabezado] el cual es un texto sin formato aparente {RVIZ}, [Volumen] el cual por el momento se estima un formato de tipo numerico 0-9 y [Copia] compartiendo el mismo valor numerico 0-9.

**ME.02** - Una Etiqueta debe de contar con los siguiente elementos como atributos:
- Atributos: EL cual es un objeto de tipo clasificacion para la separacion de atributos de un clasificacion
- Clasificacion: El cual es el argumento Clasificacion que se paso a la creacion del objeto y debe ser limpiado de cualquier tipo de basura existente en la cadena.
- Encabezado | Volumen | Copia: Los cuales son elementos que son opcionales para la construccion de un objeto en caso de no tenerse o recibir un valor invalido se pondran los siguientes valores por default respectivamente ['', '0' y '1']
- PIPE_A y PIPE_B = 2 cadenas dedicadas a la separacion de los pipes de clasificacion
- Clasificacion Valida: Bandera para el estatus de la etiqueta.
- Clasificacion Completa: Cadena que se completa utilizando todos los campos de la etiqueta. Ejemplo: RVIZU DF23.4.D23 D23 1990 V.1 C.2
#### Getters y Setters
**ME.03** - Setter de Clasificacion. Esta funcion realiza un cambio de clasificacion completa. Se realizan los siguientes pasos: Limpieza de Clasificacion (Quitar caracteres no deseados), Revisar Clasificacion se revisa si la clasificacion que se agrega es valida (se puede separar) En caso de serlo se siguen con los pasos para separar los atributos y se genera una clasificacion completa.
**ME.04** - Los setter de Volumen, Copia y Encabezado siguen el siguiente comportamiento. Si se tiene un valor valido se realizan los siguientes pasos, se obtiene el valor clave: Ejemplo de volumen V.213 --> 213 y se realiza una integracion a clasificacion completa.
#### Funcion Limpiar Clasificacion
**ME.05** - Recibe un string que se entiende que es una clasificacion y se borran de la cadena los siguiente caracteres no deseados: "LX", "MAT", "V.XXXX" y "C.XXXX" dichos caracteres no deseados se reemplazan con caracteres vacios en la cadena.

#### Funcion Revisar Clasificacion
**ME.06** - Revisa en busca de partir un string en 2 pipes por medio de los siguientes caracteres especiales " ." y ". ". Este es el caso base.
**ME.07** - En caso de no contrar con un caracter de separacion especial se toma un espacio como caracter especial el cual debe contar con las siguientes caracteristicas: Tener un numero en su lado izquierdo y tener una letra en su lado derecho.
EJEMPLO D23.5.D23 D23 1990 --> Cumple con la caracteristica en D23.5.D2**3 D**23 1990 por lo que se utiliza ese primer espacio para la separacion.
**ME.08** - En caso de que no se cumplan ninguno de estos 2 posibles separaciones de pipe se considerará erronea la clasificacion de la clase y se marcara la bandera de valido como False.
**ME.09** - En caso de completar con exito los filtros por separacion, se aplica una eliminacion de caracteres no deseados como espacios o puntos adicionales y se actualizan los atributos PIPE_A y PIPE_B con los valores, se genera una clasificacion correcta y por utlimo se marca la bandera valido como True.

#### Funcion Crear Clasificacion Completa
**ME.06** - Junta todos los atributos necesarios para generar una clasificacion completa usnado los siguientes parametros: Encabezado, Clasificacion, Volumen y Copia.
Donde el string resultante conecta todos estos parametros
#### Imprimir Modulo
**ME.06** - Imprime todos los atributos de la clase de en un solo cuadro de texto para el debugeo de la clase.

### Modulo Libro.
---
#### Incializacion.
**ML.01** - Atributos de esta clase/modulo son los siguientes:
- Titulo: titulo|Campo para ingresar el titulo completo del libro.
- Codigo de Barras: cbarras|Codigo de barras para identificar el libro.
- Identificacion / Indice: ID|ID entrada del libro con respecto al excel info.
- Etiqueta: etiqueta|Clase/Modulo que contiene los datos del libro en si.
- Estatus: estatus|Estatus del libro para identificar en la App (Valid, Error, ...)

**ML.02** - Argumentos de Inicializacion para la clase/modulo:
- Identificacion / Indice: aID|Necesario|INT numero para identificar como indice.
- Titulo: aTitulo|Necesario|String. Nombre del libro.
- Codigo de Barras: aCbarras|Necesario|string. Identificador con codigo de barras QROXXXX
- Clasificacion: aClasif|Necesario|string. clasificacion del libro. BF23.5.D23 .D23 1990
- Volumen: aVolumen|Opcional|string. numero de volumen. V.X o X. Por defecto 0.
- Copia: aCopia|Opcional|string. Numero de Copia. C.X o X. Por defecto 1.
- Encabezado: aEncabezado|Opcional|string. Encabezado opcional. RVIZ. Por defecto '' Vacio.
#### Getters y Setters.
**ML.03** - Todos los atributos son privados y unicamente se pueden acceder con getters y setters.
#### Llenar desde Excel.
**ML.04** - Cargar libros usando un archivo de Excel.
**ML.05** - Se consideran los siguientes encabezados dentro del archivo excel para una correcta obtencion de datos: Titulo, Codigo de Barras y Clasificacion. En caso de que no se encuentren estos encabezados se regresa el siguiente valor 'None'
**ML.06** - Para encontrar los 6 encabezados posibles se consideran las siguientes cadenas de texto como mas favorables dentro de un excel:
- Titulo - Titulo con o sin acento
- Codigo de Barras - Bar o codi o códi con acento
- Clasificacion - clas
- Encabezado - encab, head
- Volumen - vol
- Copia - cop
**ML.07** - Si se pasan los filtros se pasa a la siguiente seccion que es la creacion de los objetos de tipo libro usando el constructor de inicializacion correspondiente

#### Mostrar Libro.
**ML.08** - Muestra los elementos del libro dentro de una cadea de texto tipo string, hace uso de la impesion del modulo etiqueta.

### Modulo Manejo Tabla.
---
#### Inicializacion
- **MMT.01** - El Objeto Manejo Tabla no requiere nigun valor de incializacion por el momento.
- **MMT.02** - Los atributos que maneja este objeto son los siguientes:
  - Tabla Datos: Es la tabla que despliega la informacion que ve el usuario. La cual tiene la siguiente forma para sus elementos: [Clasificacion Completa | PIPE_A | PIPE_B | Estatus Libro]
  - Tabla Formato: Es la tabla encargada de guardar el formato de los elementos. Tiene el siguiente formato: [Numero Elemento (Libro) | Color] Esta tabla se maneja con los estatus que puede tener el libro.
  - Lista Libros: Es la lista que cuenta con todos los libros cargados a la aplicacion, esta no cuenta con ningun orden.
  - Lista Modificados: Esta lista contiene todos los libros que fueron modificados durante la sesion, por lo que solo se puede tener una instancia del libro en toda la lista.
  - Esatus Color: Es una lista con todos los posibles estatus que puede tomar un libro explicados a continuacion:
    - Libro Valido "Valid" #FFFFFF: Representa que un libro cumple con la norma del programa.
    - Libro con Error "Error" #F04150: Representa un libro con algun error en su clasificacion.
    - Libro Seleccionado "Selected" #498C8A: Representa un libro seleccionado para el usuario: Para esta implementacion no se usa este estatus.
    - Libro a Modificar "Modify" #E8871E: Representa un libro seleccionado para se modificado.
#### GETTERS y SETTERS
- **MMT.03** - Contamos con un getter que es para obtener la longitud de los libros cargados denominado como get_table_len()

#### Operaciones Generales de la Tabla.
---
#### Crear Tabla
- **MMT.04** - Carga todos los libros a la variable lista_libros a la aplicacion haciendo uso de la funcion del Objeto Libro llenar_desde_excel() la cual utiliza una ruta de archivo.
- **MMT.05** - Utiliza la funcion agregar_elemento() la cual utiliza los libros cargados para mostrarlos en las tablas de los atributos.
#### Revisar Tabla
- **MMT.08** - Revisa si el diccionario de libros con errores esta vacio. Si esta vacio 'True' significa que no contamos con libros con errores, caso contrario se regresa un 'False'
#### Reset Tabla
- **MMT.09** - Reinicia todos los atributos del objeto. Reinicia todo el programa.

#### Funciones de Manejo de Elementos.
---
#### Agregar Elemento.
- **MMT.06** - Con base en el estatus se le da un color al libro y esto se guarda en el elemento formato el cual cuenta con Indice Libro | Color.
- **MMT.07** - Si el libro cuenta con algun error en su Clasificacion se agrega a un diccionario secundario donde la llave sera por medio del Codigo de Barras. Esto es uando la funcion agregar_elemento_error() que usa el objeto Libro.
#### Agregar Elemento Error.
- **MMT.10** - Se agrega al diccionario de errores un libro utilizando como llave el codigo de barras del libro y cargando el libro con error.
#### Agregar Elemento Modificado
- **MMT.11** - se agregar al diccionario de libros modificados un libro, utilizando como llave el codigo de barrras del libro y cargando la siguiente estructura [El Libro y la Modificacion realizada]
#### Actualizar Datos Elemento
- **MMT.12** - Modificar la informacion de un libro por lo que debera modificar los datos vistos por el usuario y la lista de los libros cargados.
#### Actualizar Estatus Elemento
- **MMT.13** - Cambia el estatus de un libro lo cual cambia la aparencia (Color e informacion) en la pantalla que ve el usuario.


#### Operaciones Finales de la Tabla.
---
#### Ordenar Libros.





## Script GUI.py
### Modulo Ventana General
Funcionalidad para la ventana principal de la aplicacion.
**MVG.00** - Los colores de la pagina son los siguientes: Color de Fondo #3016F3, Texto #000000, Entrada y color secundario #DEE6F7
**MVG.01** - Se cuenta con una funcion llamada resource path la cual tiene la tarea de pasar todos los ASSETS a un archivo comprimido para su portabilidad/
#### Layout Izquierdo.
**MVG.02** Se requiere un boton para seleccionar un archivo de Excel, donde se muestre si se tiene un archivo seleccionado o no con la siguiente leyenda: 'Sin Archivo' al comenzar el programa o no terminar el proceso de cargado. 'Nombre del Archivo' al seleccionar un archivo de excel.
**MVG.03** - Se requiere un boton para cargar el archivo seleccionado de excel al programa.
**MVG.04** - Se consideran 2 opciones finales del programa, generar un reporte opcion 'Reporte' y generar un excel ordenado 'Excel Orden'
**MVG.05** - Se toma el logo del Tec de Monterrey y el nombre de la apliacion es 'INTERCALADOR'
**MVG.06** - Se tiene la opcion de nombrar el archivo de salida, este campo es obligatorio pero en caso de dejarse vacio se toma como base el archivo de excel cargado y se genera una copia del mismo.
#### Layout Tabla de Datos.
**MVG.07** - Se tiene una tabla donde se incluyen todos los libros cargados al programa. La tabla cuenta con las siguientes 4 columnas:
- Clasificacion: La clasificacion obtenida del libro.
- PIPE_A: Seccion de la clasificacion que contiene los siguientes posibles campos: Clase, Subdecimal y TemaEsp
- PIPE_B: Seccion de la clasificacion que contiene los siguientes posibles campos: Autor y Anio
- Estatus Libro: Se tiene el estatus general del libro con los siguientes posibles estatus. Error | Valid | Selected | Modify
**MVG.08** - Cada libro tiene la posibilidad haciendo seleccionarlo para poder modificar los atributos dentro del libro.
**MVG.09** - Un boton denominado 'Ejecutar' para ejecutar todo el ordenamiento del programa.
**MVG.10** - Un boton para reiniciar todo el programa y empezar con uno nuevo, boton 'LIMPIAR'
#### Run Window.
- **MVG.11** - Al salir del programa si no se tiene nada en la aplicacion, se cierra la aplicacion en caso se muestra un pop up para realiza un guardado del programa con la funcion guardar_programa o no guardar el progreso. Se tiene implementado un boton para poder guardar el programa cada que sea necesario.
- **MVG.19** - El programa debera poder mostrar licencias de usuario y la version que esta manejando por medio de los siguientes 
- **MVG.20** - Al presionar sobre el boton con simbolo de cargar se manda llamar la funcion seleccionar_excel() para obtener la ruta de un archivo excel y actualizar la visualizacion del programa.
- **MVG.24** - Al presionar el boton 'Cargar' se activa la funcion cargar_excel, con la cual se cargan los datos del excel seleccionado, al programa, actualizando la tabla principal del sistema.
- **MVG.28** - Al presionar el boton 'Limpiar' se reinicia el programa por completo haciendo llamar la funcion reset_window() y regresando al objeto modify_object a su estado base.
- **MVG.32** - Un elemento se puede seleccionar presionando sobre el en la tabla, este pasara por los siguientes estatus: 
  - Elementos Valido: Valid -> Modify -> Valid.
  - Elementos Erroneos: Error -> Modify -> Valid | Error.
Esto se logra con la funcion table_control(). Para seguir por estas opciones de seleccion, unicamente se puede modificar un elemento a la vez.
- **MVG.38** - Se podra modificar un elemento con el estatus 'MODIFY' de la tabla haciendo click derecho y presionando en el boton y verificando que la Bandera Modify sea 'True' para hacer uso de la funcion modificar_elemento().
- **MVG.45** - Al presionar el boton ejecutar se llama la funcion ejecutar_programa()
- **MVG.46** - Se podra desplegar mas informacion del libro si este se encuentra en un estatus 'MODIFY', esto se logra haciendo click derecho y presionando el boton 'Información'
#### Guardar programa.
- **MVG.12** - Se revisa si la tabla cuenta con contenido, en caso de no tenerlo se omite el guardado 'Sin datos para guardar'
- **MVG.13** - Se revisa si se tiene un archivo de excel base, en caso de no tenerlo se omite el guardado 'Sin Ruta para guardar'
- **MVG.14** - Se despliega un pop up (pop.save_file()) para confirmar si se desea guardar el progreso. Positivo se sigue con el programa en caso contrario se cancela el guardado 'No continuar con guardado'
- **MVG.15** - Se puede saltar el paso de preguntar con una bandera de bypass en caso de ser True, por defecto esta en False.
- **MVG.16** - Se realiza una copia del excel por temas de seguridad a la hora de guardar cualquier tipo de informacion de la aplicacion. Por lo que se toma el nombre de donde se tomaron los datos y se agrega el sufijo '_saved' para poder aclarar la copia. 
- **MVG.17** - Se utiliza una funcion guardar_libros_tabla que genera un dataframe igual al excel original agregando las correciones hechas en el programa. 
NOTA esta funcion puede no dar los resultados esperados en el caso de que se ejecute el programa para ordenar ya que no considera el orden del excel.
NOTA esta funcion puede generar un dataset con columnas adicionales debido a posibles errores de nombres.
- **MVG.18** - Se utiliza la funcion del modulo Table Manager llamada escribir_excel() para escribir el excel de salida.
- **MVG.19** - Cuando se guarde una copia con el sufijo '_saved' agregar un numero como identificador adicional. ejemplo 'excel_saved1.xlsx'
- **MVG.20** - En caso de tener el sufijo '_saved' en lugar de anadir un segundo sufijo '_saved' se anade un numero adicional
#### Seleccionar Excel.
- **MVG.21** - La funcion debera abrir un explorador de archivos para seleccionar unicamente archivos de excel.
- **MVG.22** - Posterior a la seleccion del archivo se guarda el nombre del archivo y en caso de que el proceso se cancele dicho nombre se mantiene como vacio.
- **MVG.23** - En caso de tener un nombre de archivo actualizar el elemento EXCEL_TEXT con el nombre o en caso de no contrar con una ruta u archivo poner por defecto el texto 'Sin Archivo'
#### Cargar Excel.
- **MVG.25** - Se revisa si se tiene un archivo para cargar en caso contrario activar el pop.warning_excel_file() para informar al usuario que debe seleccionar una archivo y teminar el proceso.
- **MVG.26** - En caso de tener un archivo seleccionado mandar llamar la funcion crear_tabla() del modulo Manejo Tabla, para cargar todos los libros del archivo de excel.
- **MVG.27** - Se revisa el estatus de la funcion crear_tabla() y si se da un resultado negativo 'False' se concluye que hubo un error con los encabezados. Se manda llamar un pop.error_excel_head()
- **MVG.28** - Se revisan cuantos elementos se cargaron al sistema, y en caso de superar 5000 elementos se da un aviso por medio del pop.warning_excel_size()
- **MVG.29** - Actualizar los valores de la tabla principal para mostrar los datos cargados, en conjunto con los colores correspondientes a sus estatus en este caso unicamente 2 estatus son posibles: 'Error':'#F04150', 'Valid':'#FFFFFF'.
- **MVG.30** - Ordenar todos los elementos de la tabla usando 
#### Reset Window.
- **MVG.29** - Se hace uso de la funcion reset_table() del modulo Manejo Tabla, la cual de manera resumida reinicia todos los valores de la tabla.
- **MVG.30** - Se eliminan la ruta del archivo de excel seleccionado y el nombre designado para el archivo de salida.
- **MVG.31** - Actualizar vista de la tabla a una tabla vacia.
#### Table Control.
- **MVG.33** - Si no se selecciona ningun libro valido, la funcion termina y regresa modify_object sin modificaciones.
- **MVG.34** - Se extraen los datos del libro seleccionado: INDICE En la tabla, ESTATUS que maneja el libro.
- **MVG.35** - Se actualiza el estatus del libro seleccionado usando la funcion actualizar_estatus_elemento() del modulo Manejo Tabla se pueden tener los siguientes casos:
  - Libro Valido: Valid -> Modify. Se selecciona un elemento para modificar, se guarda el estatus 'Valid' y se guarda el indice del libro 'INDEX' y se actualiza la bandera modificar a 'True'.
  - Libro Error: Error -> Modify. Se selecciona un elemento para modificar, se guarda el estatus 'Error' y se guarda el indice del libro 'INDEX' y se actualiza la bandera modificar a 'True'
  - Libro Modificar: Modify -> Valid | Modify -> Error. Para deseleccionar un elemento, se regresa al estatus anterior ('Valid'|'Error') y se libera la bandera modificar a  'False'
- **MVG.36** - Solo se puede modificar un libro a la vez por lo que se maneja una bandera para aceptar unicamente un elemento. La bandera tiene el siguiente comportamiento: 'False' sin libro a modificar. 'True' libro para modificar seleccionado.
- **MVG.37** - Se debe actualizar los estatus de los libros en la tabla principal.
#### Modificar Elemento.
- **MVG.39** - Se obtiene la informacion del modulo libro con todos sus datos.
- **MVG.40** - Se debera guardar la clasificacion previo a la modificacion por temas de reportes.
- **MVG.41** - Se despliega una ventana secundaria para modificar el libro en su totalidad.
- **MVG.42** - Si el libro se modifica se regresa un objeto de tipo Libro con todas las modificaciones, en caso de que no se modifique o se cierre la ventana se regresa un objeto de tipo 'None', si sucede este caso se cancela el proceso de modificacion y se regresa un valor 'True'.
- **MVG.43** - Cuando un libro se modifica, se debe agregar a una lista de libros modificados para tener un conteo de las modificaciones relacionadas usando la funcion agregar_elemento_modificado() del modulo Manejo Tabla.
- **MVG.44** - Una vez que se modifica el elemento este cambio se debe ver reflejado en la tabla principal. El texto y estatus. Usando las funciones actualizar_elemento() y actualizar_estatus_elemento()
- **MVG.45** - Actualizar los elementos de la tabla.
#### Ejecutar Programa.
- **MVG.46** - Se revisa si se cuenta con datos en la tabla en caso de no tenerlos el proceso de ejecucion se aborta y se muestra un mensaje en pantalla pop.warning_data().
- **MVG.47** - Se revisa si se tiene algun archivo de excel seleccionado en caso de que no se tenga ninguno seleccionado se aborta el proceso y se muestra un mensaje en pantalla pop.warning_excel_file()
- **MVG.48** - El programa requiere que se seleccione una opcion valida del proceso por lo que se debe seleccionar como minimo una opcion.
- **MVG.49** - El programa debe desplegar una opcion para seleccionar un folder donde guardar los datos que va a generar. En caso de cancelar este proceso se cancela todo el proceso de ejecucion.

## Script support_windows.py
### Modulo Ventana Modificar.
#### Inicializacion
- **MVM.01** - Para su inicializacion requiere un objeto de tipo Libro, del cual obtiene los elementos. En caso de no pararse dicho objeto se iniciaria todo el programa con elementos vacios.
#### Layout General.
- **MVM.02** - Se despliega en como enfoque principal la clasificacion completa del libro, la cual debera ser actualizada en tiempo real, pero no podra ser seleccionada por el usuario sino que debera actualizarse con las acciones y modificaciones que realiza el usuario.
- **MVM.03** - Se integra una seccion donde se puedan mostrar y modificar los siguientes elementos de la clasificacion del libro:
  - Clasificacion : Donde se planea modificar la clasificacion principal.
  - Encabezado: Donde se puede agregar un encabezado al inicio de la clasificacion completa si se desea.
  - Volumen: Seccion para modificar el valor unicamente acepta valores numericos.
  - Copia: Mismo funcionamiento que la seccion de volumen.
  - PIPE A y B, ambas secciones son de debugeo utilizados para mostrar la separacion de los atributos de la clasificacion.
- **MVM.04** - Un boton con forma de 'i' mediante el cual se podra desplegar el nombre del libro por medio de un pop up.
- **MVM.05** - 2 Botones para terminar el proceso de modificacion:
  - Cancelar: Cancela todo el proceso y no realiza absolutamente ningun cambio al libro, esta opcion debe mostrar una bandera cuando se activa.
  - Modificar: Finaliza el proceso de modificacion cambiando la clasificacion y atributos del libro. Esta opcion unicamente se activa si se cumple con una clasificacion correcta.
#### Run Window.
- **MVM.06** - Al cerrar la ventana o presionar el boton de 'Cancelar' se regresa un objeto nulo o 'None' para informar a otra interfaz que no se realizo ninguna modificacion
- **MVM.07** - Al presionar el boton 'INFO' se despliega un pop up nombrado pop.show_info_libro() para mostrar el titulo del libro.
- **MVM.08** - Al actualizar cualquier elemento posible, se actualizan 3 secciones de la ventana: Clasificacion Completa 'CLAS_FULL', PIPE_A y PIPE_B 'PIPE_A' 'PIPE_B' y El boton Modificar que se habilita con base en el estatus del libro. Todo esto se logra con la funcion actualizar_ventana()
- **MVM.09** - Al presionar el boton Modificar este cierra la ventana y regresa el libro modificado. por completo.



## Requerimientos Nuevos.
- **RN.00** - Pasar los libros erroneos hasta el principio. Ordenar en la interfaz los libros con clasificacion correcta. Se logra por medio del objeto Clasificacion ya que los atributos estan estandarizandos para irse al tope por medio de la cadena A000
- **RN.01** - Agregar la opcion de poder mostrar el titulo del libro seleccionado.