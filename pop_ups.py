from tkinter import messagebox


# # ? POP_up de advertencia (Warning)
##########################################################
def warning_excel_file():
  msg = f'!Fallo!\nSeleccione un archivo de Excel'
  messagebox.showwarning("No Excel File", msg)

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
##########################################################

# # ? POP_up de Error (Error)
##########################################################
def error_excel_file():
  msg = f'!Fallo!\n Ninguna Etiqueta se cargo'
  messagebox.showerror("Excel File Error", msg)

def error_manual_order():
  msg = f'!Fallo!\n No se puede ordenar'
  messagebox.showerror("", msg)
##########################################################

# # ? POP_up de Informacion (Info)
##########################################################
def success_program():
  msg = f'Felicidades\n El programa finalizó con exito'
  messagebox.showinfo('', msg)

def not_enough_books():
  msg = f'Poca Cantidad de Libros \n Itercale a manualmente'
  messagebox.showinfo('', msg)

def success_manual_order():
  msg = f'Felicidades\n Librero Ordenado Correctamente'
  messagebox.showinfo('', msg)

def info_license():
  msg = f'Programa Bajo Licencia del Tecnológico de Monterrey\n !No reproducir sin permiso!'
  messagebox.showinfo("Licencia", msg)

def info_about():
  msg = f'Programa Generador de Etiquetas\n Por: Jesus Talamantes Morales 2022'
  messagebox.showinfo("About", msg)

def show_info_libro(titulo:str):
  msg = f'Título del Libro:\n {titulo}'
  messagebox.showinfo("Book Info", msg)

# # ? POP_up de OkCancel Ask (askokcancel)
##########################################################
def check_images():
  msg = f'Imágenes Generadas\n Presione Aceptar para continuar con su PDF'
  answer = messagebox.askokcancel("Confirmar", msg)
  return answer

if __name__ == "__main__":
  print(check_images())



