from tkinter import *
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import Main_Intercarlador as inter

version = "6.0"
root = Tk()
root.title('Intercalador')  # Encabezado
root.iconbitmap('Assets/book_icon.ico')
root.resizable(width=False, height=False) # No se puede modificar el tamaño

archivo = ''
carpeta = ''
reporte = IntVar()
reporteExcel = IntVar()
reporteError = IntVar()
opcionesReporte = [0,0,0]

def opcionesProg():
    global opcionesReporte
    if reporte.get() == 1:
        opcionesReporte[0] = 1
    if reporteExcel.get() == 1:
        opcionesReporte[1] = 1
    if reporteError.get() == 1:
        opcionesReporte[2] = 1

def infoAdicional():
    messagebox.showinfo("Intercalador Tec", 
                        "Procesador de Excels. \nVersion " + version + " 2022 \nDesarollado: Jesus David Talamantes Morales"
                        )
def avisoLicencia():
    messagebox.showwarning("Licencia", 
                           "Producto bajo licencia del \n Tecnologíco de Monterrey"
                           )
def salirApp():
    #valor = messagebox.askquestion("Salir ?", "¿Deseas Salir de la APP?")
    valor = messagebox.askokcancel("Salir ?", "¿Deseas Salir de la APP?")
    if valor == True: root.destroy()

def abrirArchivo():
    global archivo
    direccionText.delete(0,END)
    archivo = ''
    archivo = filedialog.askopenfilename(title="Abrir Archivo Excel",
                                         filetypes=(("Excel File","*.xlsx"),("Todos los Archivos","*.*")))
    direccionText.insert(0,archivo)

def abrirCarpeta():
    global carpeta
    carpetaText.delete(0,END)
    carpeta = ''
    carpeta = filedialog.askdirectory(title="Carpeta de Salida")
    carpetaText.insert(0,carpeta)

def ejecutarPrograma():
    nombre = ''
    nombre = str(nombreText.get())
    if archivo == '':
        messagebox.showwarning("Archivo Excel",
                               "Porfavor!! \nSeleccione un Archivo de Excel")
    elif carpeta == '':
        messagebox.showwarning("Carpeta de Salida",
                               "Porfavor!! \nSeleccione una Carpeta de Salida")
    elif nombre == '':
        messagebox.showwarning("Nombre del Archivo",
                               "Porfavor!! \nDele nombre al archivo de Salida")
    elif opcionesReporte[0] + opcionesReporte[1] + opcionesReporte[2] == 0:
        messagebox.showwarning("Opciones",
                               "Porfavor!! \nSeleccione una Casilla")
    else:
        Estatus = inter.main_program(archivo=archivo, carpeta=carpeta, nombre=nombre, reporte=opcionesReporte, codify=0)
        if Estatus == False:
            messagebox.showerror("Error Datos Excel",
                                 "Error en el reporte Excel \nFalla en encontrar columna Calsificación \nrevisar tutoriales")
        else:
            messagebox.showinfo("Exito en Ejecución",
                                "El Programa Finalizó exitosamente !!!")


#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
image = Image.open("Assets/LogoTec2.png")
# Resize the image using resize() method
resize_image = image.resize((200, 60))
img = ImageTk.PhotoImage(resize_image)

barraMenu = Menu(root)
root.config(menu=barraMenu)

archivoMenu = Menu(barraMenu, tearoff=0)
archivoMenu.add_command(label="Salir", command=salirApp)

archivoAyuda = Menu(barraMenu, tearoff=0)
archivoAyuda.add_command(label="Tutoriales")
archivoAyuda.add_command(label="Licencia", command=avisoLicencia)
archivoAyuda.add_command(label="Acerca de ...", command=infoAdicional)

barraMenu.add_cascade(label="Programa", menu=archivoMenu)
barraMenu.add_cascade(label="Ayuda", menu=archivoAyuda)

canvas = Canvas(root, height=450, width=900, bg='#3016F3')
canvas.pack()

frame = Frame(root, bg="white")
frame.place(relwidth=0.9, relheight=0.9, relx=0.05, rely=0.05)

titleLabel = Label(frame, text="Intercalador")
titleLabel.config(font=("Open Sans", 24, "bold", "italic"), justify="center", bg="white")
titleLabel.grid(row=0, column=0, columnspan=2, sticky="NSEW", padx=10, pady=5)

imageLabel = Label(frame, image=img, bg="white")
imageLabel.grid(row=0, column=2, sticky="NSEW", padx=10, pady=5)

cargarButton = Button(frame, text="Abrir Archivo", command=abrirArchivo)
cargarButton.config(font=("Open Sans", 14), justify="right", bg="white")
cargarButton.grid(row=2, column=0, sticky="E", padx=2, pady=10)

direccionText = Entry(frame, width=65)
direccionText.config(borderwidth=5, font=("Open Sans", 11), bg="#DEE6F7", justify="center")
direccionText.grid(row=2, column=1, columnspan=2,
                   sticky="NSEW", pady=10, padx=10)

directorioButton = Button(frame, text="Abrir Carpeta", command=abrirCarpeta)
directorioButton.config(font=("Open Sans", 14), justify="right", bg="white")
directorioButton.grid(row=3, column=0, sticky="E", padx=2, pady=10)

carpetaText = Entry(frame, width=65)
carpetaText.config(borderwidth=5, font=("Open Sans", 11),
                   bg="#DEE6F7", justify="center")
carpetaText.grid(row=3, column=1, columnspan=2,
                 sticky="NSEW", pady=10, padx=10)

nombreLabel = Label(frame, text="Nombre Archivo")
nombreLabel.config(font=("Open Sans", 14), justify="right", bg="white")
nombreLabel.grid(row=4, column=0, sticky="E", padx=5, pady=10)

nombreText = Entry(frame, width=25)
nombreText.config(borderwidth=5, font=("Open Sans", 14),
                   bg="#DEE6F7", justify="center")
nombreText.grid(row=4, column=1, sticky="NSEW", pady=10, padx=10)

reporteCheck = Checkbutton(frame, text="Reporte")
reporteCheck.config(bg="white", font=("Open Sans", 14), justify="center",
                    variable=reporte, onvalue=1, offvalue=0, command=opcionesProg)
reporteCheck.grid(row=5, column=0, sticky="NSEW", pady=10, padx=2)

excelCheck = Checkbutton(frame, text="Excel Ord.")
excelCheck.config(bg="white", font=("Open Sans", 14), justify="center",
                  variable=reporteExcel, onvalue=1, offvalue=0, command=opcionesProg)
excelCheck.grid(row=6, column=0, columnspan=2, sticky="NSEW", pady=10, padx=2)

errorCheck = Checkbutton(frame, text="Excel Error Ord.")
errorCheck.config(bg="white", font=("Open Sans", 14), justify="center", 
                  variable=reporteError, onvalue=1, offvalue=0, command=opcionesProg)
errorCheck.grid(row=5, column=1, sticky="NSEW", pady=10, padx=2)

ejecutarButton = Button(frame, text="Ejecutar", command=ejecutarPrograma)
ejecutarButton.config(font=("Open Sans", 14), bg="white")
ejecutarButton.grid(row=6, column=2, sticky="NSEW", pady=10, padx=5)



root.mainloop()