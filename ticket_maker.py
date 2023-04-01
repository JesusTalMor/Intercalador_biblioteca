import os

from fpdf import FPDF
from PIL import Image, ImageDraw, ImageFont

import pop_ups as pop

# TODO Ajustar el encabezado 1 cm de margen, listo pero no me convence
# TODO Queda pendiente PNG o PDF - Dejar en PNG etiquetas individuales

alphabet = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
# * Tipografia de la etiquetas
FONT_SIZE = 40
MAIN_FONT = ImageFont.truetype("Assets/Khmer OS Muol.otf", size=FONT_SIZE)
ESCALA = 100  #? Escala de la etiqueta recomendado 100
COLOR = "rgb(0, 0, 0)"


def max_len_list(lista: list) -> int:
  max_len = 0
  for texto in lista:
    max_len = len(texto) if len(texto) > max_len else max_len
  return max_len


def separar_STR(STR:str):
  """ Separa un Clasificación y retorna una lista"""
  lista_salida = []
  # * Separar por espacios separa PIPE A de PIPE B y la anterior en autor y año
  space_list = STR.split(' ')  
  # Ejemplo 'PQ7298.424.A76 .O744 2007' -> [PQ7298.424.A76] [.O744] [2007]
  #* Separa el PIPE A en sus atributos: Categorias XD
  pipe_a = space_list.pop(0) 
  # Ejemplo [PQ7298.424.A76] [.O744] [2007] -> [PQ7298.424.A76] | [.O744] [2007]
  pipe_a = pipe_a.split('.') 
  # Ejemplo [PQ7298.424.A76] -> [PQ7298] [424] [A76]
  letras_tema = pipe_a.pop(0)
  # Ejemplo [PQ7298] [424] [A76] -> [PQ7298] | [424] [A76]
  # print(space_list, pipe_a, letras_tema, sep='\n')
  #* Trabajar en separar letras y numeros
  letras_tema = [letras_tema[:2], letras_tema[2:]] if letras_tema[1] in alphabet else [letras_tema[0][:1], letras_tema[0][1:]]
  # Ejemplo PQ7298 -> [PQ, 7298] si 2 letras otro caso P7298 -> [P, 7298]
  # print(space_list, pipe_a, letras_tema, sep='\n')
  #* Juntar todas las listas en la salida
  lista_salida.extend(letras_tema)
  lista_salida.extend(pipe_a)
  lista_salida.extend(space_list)
  # Ejemplo [PQ, 7298] + [424, A76] + [.O744, 2007] -> ['PQ', '7298', '424', 'A76', '.O744', '2007']
  # print('Entrada', STR, sep='\n')
  # print('Salida Final', lista_salida, sep='\n')
  return lista_salida


def separate_list(str_dict: dict):
  """ Recibe un diccionario y crea una lista para imprimir """
  lista_salida = []
  #* Usando un diccionario obtener todos los elementos
  encabezado = [str_dict['HEAD']]
  clasif = separar_STR(str_dict["CLASS"])
  volumen = [str_dict['VOL']] if 'V.' in str_dict['VOL'] else ['']
  copia = ['C.' + str_dict['COP']] if str_dict['COP'] not in ('1', '0', '', ' ') else ['']
  #* Juntar todos los elementos
  lista_salida.extend(encabezado)
  lista_salida.extend(clasif)
  lista_salida.extend(volumen)
  lista_salida.extend(copia)
  #* Limpiar elementos vacios
  # lista_salida = [x for x in lista_salida if x != '']
  # print('Entrada', str_dict, sep='\n')
  # print('Salida', lista_salida, sep='\n')
  return lista_salida


def imprimir_etiqueta(lista_a_imprimir: list, config: dict, ruta: str, titulo:str, num=0000):
  ''' 
    Genera una imagen PNG de la Etiqueta de un Libro
    ! Sujeto a posibles cambios a futuro

    NOTAS:
    Sin modificar el FONT_SIZE de 40, en la etiqueta, común entran 8 filas, para una altura de 370 pxl.

  '''
  global FONT_SIZE
  # TODO Podemos recibir los parametros y hacer la conversión aqui Me gusta mas esta
  #* Configuración de la Etiqueta
  IW, IH = config['TW'], config['TH']

  #* Medidas en pixeles de la etiqueta
  img_width = int(ESCALA * float(IW))
  img_height = int(ESCALA * float(IH))
  print('Medidas Etiqueta pxl. ', ('Alto', img_height), ('Ancho', img_width))
  
  max_len = max_len_list(lista_a_imprimir)
  print('largo maximo a imprimir: ', max_len)
  
  #* Variables para posicionarse
  limpiar_lista = [x for x in lista_a_imprimir if x != '']
  FONT_SIZE = 35 if len(limpiar_lista) > 8 else 40 
  real_font_size = (FONT_SIZE * 0.6) 
  # row_diff = 8 - len(lista_a_imprimir)
  jump_size = FONT_SIZE * 1.125
  superior_border =  -(FONT_SIZE * 0.3)
  
  #* Posicion del cursor para escribir
  Y_pos = superior_border
  X_pos = (img_width/2) - ((max_len/2) * real_font_size)

  #* Llenado de la etiqueta
  main_img = Image.new("RGB", (img_width, img_height), color=(255, 255, 255))
  image_draw = ImageDraw.Draw(main_img) # objeto para dibujar
  #* Imprime todo el texto en una imagen
  y_print = Y_pos # Posicion del encabeza
  for texto in lista_a_imprimir:
    image_draw.text((X_pos, y_print), texto, fill=COLOR, font=MAIN_FONT)
    y_print += jump_size
  #* Guardar la imagen
  ruta_img = f'{ruta}/{num}_{titulo}.png'
  main_img.show()
  main_img.save(ruta_img)


def imprimir_pagina(etiquetas_a_imprimir:list, lista_a_imprimir: list, config: dict, ruta: str, titulo:str):
  fpdf = FPDF() # Objeto para crear pdfs
  lista_imagenes_auxiliares = []
  #? Llenado de la pagina
  #* Generamos una nueva pagina en blanco
  main_img = Image.new("RGB", (Pwidth, Pheight), color=(255, 255, 255))
  image_draw = ImageDraw.Draw(main_img) # Objeto para dibujar en la imagen
  
  #* Posición inicial para el cursor
  y, x = position
  page_counter = 0
  for etiqueta in etiquetas_a_imprimir:  
    #* Cambio de Linea - Se terminan las columnas
    if x == int(COL):  
      x = 0
      y += 1

    #* Cambio de página - Se terminan las filas
    if y == int(ROW):
      ruta_img = f'{ruta}/{page_counter}_aux_image.png'
      main_img.show()
      main_img.save(ruta_img) # Guardar imagen actual
      lista_imagenes_auxiliares.append(ruta_img) # Agregar imagen a cola de imagenes
      
      #* Generamos una nueva pagina en blanco
      main_img = Image.new("RGB", (Pwidth, Pheight), color=(255, 255, 255))
      image_draw = ImageDraw.Draw(main_img)

      #* Nueva posición inicial para el cursor
      y, x = 0, 0
      page_counter += 1

    #* Imprimir contenido de etiqueta
    # Cursor para etiqueta individual
    x_print = X_pos + (Iwidth * x)
    y_print = Y_pos + (Iheight * y)
    
    for text in etiqueta:
      image_draw.text((x_print, y_print), text, fill=COLOR, font=MAIN_FONT)
      y_print += 45
    #* Cambio de Columna
    x += 1  

  # * Muestreo de la Imagen (Guardar Imagen)
  ruta_img = f'{ruta}/{page_counter}_aux_image.png'
  main_img.show()
  main_img.save(ruta_img) # Guardar imagen actual
  lista_imagenes_auxiliares.append(ruta_img) # Agregar imagen a cola de imagenes
  
  
  # Mostrar pop up de confirmación
  answer = pop.check_images()
  if answer:
    for index in range(page_counter+1):
      fpdf.add_page()
      aux_image = f"{root}/{index}_aux_image.png"
      fpdf.image(aux_image, 0,0, w=210)
      os.remove(aux_image)
    fpdf.output(root + "/" + str(date) + ".pdf")
  else:
    for index in range(page_counter+1):
      aux_image = f"{root}/{index}_aux_image.png"
      os.remove(aux_image)


def ticket_maker_main(etiquetas_a_imprimir: list, titulo: str, ruta:str, config:dict, position:tuple):
  """
  
  Toma una lista de strings y genera imagenes ya sean formato PNG o PDF.
  
  :param str_list: 
    Es una lista que contiene las cadenas a imprimir
    Ejemplo Entrada: ['ARVIZU', 'HG4551 .R8 2010', 'V.2', '2']
  :param titulo: 
    Nombre para ponerle al archivo de salida
  :param root: La ruta de guardado de los archivos generados
  :param config: La configuración de las imagenes que se generarán
  :param position: !Solo caso de Tamaño carta! Posición de inicio para imprimir
  """
  
  #* Tranforma la lista de diccionarios a una lista para imprimir
  lista_a_imprimir = [separate_list(elem) for elem in etiquetas_a_imprimir]

  # # * Recibe la configuración para las etiquetas
  # PW, PH = config['PW'], config['PH'] 
  # IW, IH = config['TW'], config['TH']
  COL, ROW = config['PC'], config['PR']
    
  # # * (Individual) Medidas de Etiqueta
  # Iwidth = int(scale * float(IW))
  # Iheight = int(scale * float(IH))
  # # * Hoja Completa Medidas Hoja
  # Pwidth = int(scale * float(PW))
  # Pheight = int(scale * float(PH))

  # # * Margen en eje Y
  # Y_pos = int(0.6*scale) # Ajuste de margen ya definido
  # # * Calcular la posición del cursor en X
  # X_pos = int(Iwidth / 2) - 40


  if int(COL) != 0:
    pass
  #? Imprimir etiquetas individuales
  else:
    for ind, etiqueta in enumerate(lista_a_imprimir):
      imprimir_etiqueta(
        lista_a_imprimir=etiqueta, config=config, ruta=ruta, 
        titulo=titulo, num=ind)



if __name__ == "__main__":
  main_list = {'HEAD': '', 'CLASS':'BF109.78.J89 .C791 2010', 'VOL':'', 'COP':'1'}
  print(separate_list(main_list))
  