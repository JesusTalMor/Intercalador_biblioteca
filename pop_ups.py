from tkinter import messagebox


# # ? POP_up de advertencia (Warning)
##########################################################
def warning_excel_file():
  msg = f'!Fallo!\nSeleccione un archivo de Excel'
  messagebox.showwarning("No Excel File", msg)

def warning_excel_size():
  msg = f'!Advertencia!\nSe superaron los elementos recomendados para la aplicación.\n Se recomiendan menos de 5000 Elementos.'
  messagebox.showwarning("Excel Size Warning", msg)

def warning_excel_used():
  msg = f'!Advertencia!\nUn archivo de excel ya se encuentra en uso.\n Presione Limpiar si desea cargar otro archivo.'
  messagebox.showwarning("Excel Size in Use", msg)

def warning_excel_file_data_error():
  msg = f'!Advertencia!\n Algunas Etiquetas no logran cargarse'
  messagebox.showwarning("File Data Warning", msg)

def warning_folder():
  msg = f'!Fallo!\nSeleccione una carpeta de Salida'
  messagebox.showwarning("No Folder", msg)

def warning_name():
  msg = f'!Advertencia!\n Dele nombre al archivo de Salida'
  messagebox.showwarning("No Name", msg)

def warning_option():
  msg = f'!Advertencia!\n Seleccione alguna opción'
  messagebox.showwarning("No Option", msg)

def warning_clas():
  msg = f'!Advertencia!\n Algunas clasificaciones tienen error.\n Modifique para continuar'
  messagebox.showwarning("Some Clas Errors", msg)

def warning_data():
  msg = f'!Fallo!\n Cargue los datos porfavor.'
  messagebox.showwarning("No Data", msg)

##########################################################

# # ? POP_up de Error (Error)
##########################################################
def error_excel_file():
  msg = f'!Fallo!\n Ninguna Etiqueta se cargo'
  messagebox.showerror("Excel File Error", msg)

def error_excel_head():
  msg = f'!Fallo!\n No se lograron ubicar los encabezados necesarios. \n Agregar [Clasificación | C. Barras | Título]'
  messagebox.showerror("Excel File Error Head", msg)

def error_manual_order():
  msg = f'!Fallo!\n No se puede ordenar'
  messagebox.showerror("", msg)
##########################################################

# # ? POP_up de Informacion (Info)
##########################################################
def success_program(ruta):
  msg = f'Felicidades\n El programa finalizó con exito\n El Archivo se encuentra en:\n{ruta}'
  messagebox.showinfo('Program Finished', msg)

def not_enough_books():
  msg = f'Poca Cantidad de Libros \n Itercale a manualmente'
  messagebox.showinfo('', msg)

def success_manual_order():
  msg = f'Felicidades\n Librero Ordenado Correctamente'
  messagebox.showinfo('', msg)

def info_license():
  msg = f'Programa Bajo Licencia del Tecnológico de Monterrey\n !No reproducir sin permiso!'
  messagebox.showinfo("Licencia", msg)

def info_about(version):
  msg = f'Programa Generador de Etiquetas\nVersión: {version}\nPor: Jesus Talamantes Morales 2022'
  messagebox.showinfo("About", msg)

def show_info_libro(titulo:str):
  msg = f'Título del Libro:\n {titulo}'
  messagebox.showinfo("Book Info", msg)

# # ? POP_up de OkCancel Ask (askokcancel)
##########################################################
def check_images():
  msg = f'Presione Aceptar para generar su PDF'
  answer = messagebox.askokcancel("Generador IMG", msg)
  return answer

def save_file():
  msg = f'Desea guardar su progreso ?'
  answer = messagebox.askokcancel("Save Progress", msg)
  return answer

if __name__ == "__main__":
  print(check_images())



