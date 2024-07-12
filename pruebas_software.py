from managers import Clasificacion


def prueba_clasificacion():

  lista_pruebas1 = [
    ['', 'M48 1998'],
    ['BF76.5.G89', ''],
    ['BF76.5.G89','M48 1998'],
    ['BF76','M48'],
    ['BF76.5','1998'],
    ['BF76.5.G89','M48'],
    ['BF76.5.G89','1998'],
  ]

  lista_pruebas2 = [
    ['BF76', True],
    ['BF76', False],
    ['BFD769', True],
    ['BFD768', False],
  ]  
  etiqueta = Clasificacion()
  print(etiqueta)

  etiqueta.sacar_atributos('', '')
  print(etiqueta)

  texto = 'BF76.5.G89 M48 1998'
  for PIPE_A, PIPE_B in lista_pruebas1:
    etiqueta = Clasificacion()
    etiqueta.sacar_atributos(PIPE_A, PIPE_B)
    print(etiqueta)

  
  texto = 'BF76'
  for text, flag in lista_pruebas2:
    etiqueta = Clasificacion()
    print(etiqueta.estandarizar(text, flag))

if __name__ == '__main__':
  prueba_clasificacion()
