import re

from managers import Clasificacion, Etiqueta, Libro
from support_windows import VentanaModificar


def prueba_clasificacion():

  lista_pruebas1 = [
    ['', 'M48 1998'],
    ['BF76.5.G89', ''],
    ['BF76.5.G89','M48 1998'],
    ['BF76','M48'],
    ['BF76.5','1998'],
    ['BF76.G89','M48'],
    ['BF76.5.G89','1998'],
  ]

  lista_pruebas2 = [
    ['HD85', True],
    ['HD6331', True],
    ['HD9014', True],
    # ['BFD768', False],
  ]  
  etiqueta = Clasificacion()
  print(etiqueta)

  etiqueta.sacar_atributos('', '')
  print(etiqueta)

  texto = 'BF76.5.G89 M48 1998'
  for PIPE_A, PIPE_B in lista_pruebas1:
    etiqueta = Clasificacion()
    print(PIPE_A, PIPE_B)
    etiqueta.sacar_atributos(PIPE_A, PIPE_B)
    print(etiqueta)
    etiqueta.estandarizar_atributos()
    print(etiqueta)

  
  texto = 'BF76'
  for text, flag in lista_pruebas2:
    etiqueta = Clasificacion()
    print(etiqueta.estandarizar(text, flag))


def prueba_etiqueta():
  # Inicializacion del Objeto.
  etiqueta = Etiqueta()
  print(etiqueta)
  etiqueta = Etiqueta(
    aClasif='BF39.5.D23 .D23 1990  LX  MAT  V.123C.2421', 
    aEncabezado='nan', 
    aVolumen='V.12',
    aCopia='C.15',
  )
  print(etiqueta)

  # Objeto Clasificacion PROBADO
  # Funcion Limpiar Clasificacion
  lista_pruebas = [
  'BF39.5.D23 .D23 1990 LX',
  'BF39.5.D23 .D23 1990LX',
  'BF39.5.D23 .D23 1990MAT',
  'BF39.5.D23 .D23 1990 MAT',
  'BF39.5.D23 .D23 1990 V.1',
  'BF39.5.D23 .D23 1990 V.1123',
  'BF39.5.D23 .D23 1990 C.1',
  'BF39.5.D23 .D23 1990 C.2345',
  'BF39.5.D23 .D23 1990 LX MAT V.1 C.2',
  'BF39.5.D23 .D23 1990LXMATV.1C.2',
  'BF39.5.D23 .D23 1990  LX  MAT  V.123C.2421',
  ]
  for prueba in lista_pruebas:
    print('Entrada', prueba)
    print('Salida', etiqueta.limpiar_clasif(prueba), '\n')
  
  
  # Funcion Revisar Clasificacion
  lista_pruebas = [
    'BF 39.5.D23 D23 1990',
    'BF39.5.D23 D23.1990',
    'BF109.V95 .J69 2002'
  ]
  for prueba in lista_pruebas:
    print('Entrada', prueba)
    print('Resultado', etiqueta.revisar_clasif(prueba))
  # Funcion LLenar Atributos - PROBADO.
  # Funcion Crear Clasificacion Completa.

def prueba_libro():
  ruta = 'C:/Users/EQUIPO/Downloads/Intercalador desordenado.xlsx'
  # ruta = 'C:/Users/EQUIPO/Downloads/Intercalador ordenado.xlsx'
  lista_libros = Libro.llenar_desde_excel(ruta)
  total = len(lista_libros)
  cuenta_pos = 0
  cuenta_neg = 0
  for libro in lista_libros:
    if libro.etiqueta.clasif_valida is True:
      cuenta_pos += 1
    else:
      cuenta_neg += 1
  
  print(
    f"""
    Estadisticas:
    Total de libros {total}
    En regla: {cuenta_pos}|{(cuenta_pos/total)*100:.2f}%
    Con error: {cuenta_neg}|{(cuenta_neg/total)*100:.2f}%
    """)
  
  print(lista_libros[476])

def prueba_modificar():
  libro_prueba = Libro(
    aID=1,
    aTitulo='Libro Prueba', 
    aCbarras='QRO0001', 
    aClasif='HF23.3.D23 1920 .I22 1990',
    aVolumen='V.5',
    aCopia='C.2',
    aEncabezado='TEXTO')
  
  print(f'[DEBUG] {libro_prueba}')

  V = VentanaModificar(libro_prueba)
  resultado = V.run_window()
  print(f'[DEBUG] Salida {type(resultado)}')
  print(resultado)

  """
  Historia del toreo / Jorge Laverón -> 2 TABS
  Historia del toreo en México : época colonial, 152
  ...O llevarás luto por mí / Dominique Lapierre, La
  """

if __name__ == '__main__':
  # prueba_clasificacion()
  # prueba_etiqueta()
  # prueba_libro()
  prueba_modificar()
