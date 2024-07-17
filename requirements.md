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
**MMT.01** - Atributos de la clase
#### Crear Tabla
**MMT.02** - Genera la tabla de los libros, carga todos los libros desde una ruta para un archivo de Excel utiliza la funcion agregar elemento.



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
**MVG.11** - Al salir del programa si no se tiene nada en la aplicacion, se cierra la aplicacion en caso se muestra un pop up para realiza un guardado del programa con la funcion guardar_programa o no guardar el progreso.
#### Guardar programa.
- **MVG.12** - Se revisa si la tabla cuenta con contenido, en caso de no tenerlo se omite el guardado 'Sin datos para guardar'
- **MVG.13** - Se revisa si se tiene un archivo de excel base, en caso de no tenerlo se omite el guardado 'Sin Ruta para guardar'
- **MVG.14** - Se despliega un pop up (pop.save_file()) para confirmar si se desea guardar el progreso. Positivo se sigue con el programa en caso contrario se cancela el guardado 'No continuar con guardado'
- **MVG.15** - Se puede saltar el paso de preguntar con una bandera de bypass en caso de ser True, por defecto esta en False.
- **MVG.16** - Se realiza una copia del excel por temas de seguridad a la hora de guardar cualquier tipo de informacion de la aplicacion. Por lo que se toma el nombre de donde se tomaron los datos y se agrega el sufijo '_saved' para poder aclarar la copia. 
- **MVG.17** - Se utiliza una funcion guardar_libros_tabla que genera un dataframe igual al excel original agregando las correciones hechas en el programa. 
NOTA esta funcion puede no dar los resultados esperados en el caso de que se ejecute el programa para ordenar ya que no considera el orden del excel.
NOTA esta funcion puede genear un dataset con columnas adicionales debido a posibles errores de nombres.
- **MVG.18** - Se utiliza la funcion del modulo Table Manager llamada escribir_excel() para escribir el excel de salida.


