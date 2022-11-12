import pandas as pd
from pandas import ExcelWriter

from ApoyoSTRLIST import *
from AtributeManager import *

'''
    Funciones para correr programa Descarte
'''

def cargarExcel(path):
    '''
        Funcion para cargar un archivo de tipo Excel \n
        @path: Es el camino del archivo debe estar en path absoluto
        @return: Una lista con los valores de clasificación
    '''
    #io = "Nombre del Archivo o Direccion del mismo"
    #sheet_name = "Nombre de la Pagina" Especificar Nombre o integer para que vaya de 1 en 1 [0,1, "B"]
    try:
        Datos = pd.read_excel(path,sheet_name=None)
        return Datos
    except:
        print(F'Ocurrió un error al abrir el archivo')
        return False


def cargarDatos(dataframe):
    '''
        Funcion de chequeo de datos para Ordenar
        @dataframe: Un data frame con llaves
        @return: 2 Listas de datos Clasificacion y C.Barras
    '''
    lClas = [False]
    lVol = [False]
    lCop = [False]
    lName = [False]
    lCBarras = [False]

    llaves = list(dataframe)
    # print(llaves)
    if 'Clasificación' in llaves and 'Volumen' in llaves and 'Copia' in llaves:
        lClas = dataframe['Clasificación']
        lVol = dataframe['Volumen']
        lCop = dataframe['Copia']
        if 'C. Barras' in llaves: lCBarras = dataframe['C. Barras']
        if 'Título' in llaves: lName = dataframe['Título']
    return lClas, lVol, lCop,  lName, lCBarras


def analisisCasosIdeales(STR, STR_C, STR_V, x, lisMain, STR_clas, codify):
    '''
        Funcion para realizar analisis de clasificacion
        @STR: Recibe una cadena con la clasificacion del libro
        @STR_C: Recibe el valor de la copia del libro
        @STR_V: Recibe el valor del volumen del libro
        @X: Recibe un valor INT referente al indice
        @lisMain: Recibe una lista de diccionarios donde almacena la clasificacion ya separada
        @STR_clas: Recibe una cadena con la clasificación completa
    '''
    if revisarSep(STR) and revisarPipeB(STR):
        lisMain.append(caso_ideal(STR, STR_C, STR_V, STR_clas, x, codify))
        return True
    else: return False


def limpiarLista(lista_Main,llaves):
    '''
        Funcion para limpiar los parametros de una lista de diccionarios, donde \n
        se recibe una lista con diccionarios y posteriormente se limpia cada \n
        llave de los mismos quitando caracteres como [ , .]
        @lista_Main: Recibe una lista con diccionarios
        @Return: La misma lista pero sin caracteres no deseados
    '''
    # Variables de Tamaño de Arreglo
    ML_all = [0,0,0,0]
    length = len(lista_Main)
    for ind in range(length):
        if llaves[0] in lista_Main[ind]:
            #Limpiando Clase
            STRaux = Limpieza(lista_Main[ind][llaves[0]])
            ML_all[0] = MaxCheck(ML_all[0],len(STRaux))
            lista_Main[ind][llaves[0]] = STRaux
        if llaves[1] in lista_Main[ind]:
            #Limpiando SubDecimal
            STRaux = Limpieza(lista_Main[ind][llaves[1]])
            ML_all[1] = MaxCheck(ML_all[1],len(STRaux))
            lista_Main[ind][llaves[1]] = STRaux
        if llaves[2] in lista_Main[ind]:
            #Limpiando Tema Especial
            STRaux = Limpieza(lista_Main[ind][llaves[2]])
            ML_all[2] = MaxCheck(ML_all[2],len(STRaux))
            lista_Main[ind][llaves[2]] = STRaux
        if llaves[3] in lista_Main[ind]:
            #Limpiando Autor
            STRaux = Limpieza(lista_Main[ind][llaves[3]])
            ML_all[3] = MaxCheck(ML_all[3],len(STRaux))
            lista_Main[ind][llaves[3]] = STRaux  
        if llaves[4] in lista_Main[ind]:
            #Limpiando Autor
            lista_Main[ind][llaves[4]] = Limpieza(lista_Main[ind][llaves[4]])  
    return lista_Main, ML_all


def estandarizarLista(lista_Main,MLC,MLSD,MLTE,MLA,llaves):
    '''
        Funcion para estandarizar todas las llaves de los diccionarios \n
        @Lista_Main: Recibe una lista con diccionarios a estadarizar
        @MLT: Recibe el largo maximo para el parametro Tema
        @MLA: Recibe el largo maximo para el parametro Autor
        @MLS: Recibe el largo maximo para el parametro Subtema
        @Return: Una lista estandarizada
    '''
    length = len(lista_Main)
    for ind in range(length):
        #Estandarizando Clase
        if llaves[0] in lista_Main[ind]: 
            STR = lista_Main[ind][llaves[0]]
            # print(Estandarizar(STR,MLC))
            lista_Main[ind][llaves[0]] = Estandarizar(STR,MLC)
        #Estandarizando Subdecimal
        if llaves[1] in lista_Main[ind]:
            STR = lista_Main[ind][llaves[1]]
            lista_Main[ind][llaves[1]] = Estandarizar(STR,MLSD)
        # Estandarizando Tema especial
        if llaves[2] in lista_Main[ind]: 
            STR = lista_Main[ind][llaves[2]]
            lista_Main[ind][llaves[2]] = Estandarizar(STR,MLTE)
        #Estandarizando Autor
        if llaves[3] in lista_Main[ind]:
            STR = lista_Main[ind][llaves[3]]
            lista_Main[ind][llaves[3]] = Estandarizar(STR,MLA)
    return lista_Main


def ordenarLista(lisMain,llaves,i):
    '''
        Funcion que recibe una lista de diccionarios semi
        ordenados y los ordena por llaves
        @lisMain: Una lista semi ordenada de diccionarios
        @llaves: Vector de llaves ordenadas
        @i: Iterador para vector
        @Return: una lista ordenada con base a la llave
    '''
    lenght = len(lisMain)
    lista_ORD = []
    # Crea Grupos de Temas
    start_index = 0
    while start_index < lenght:
        final_index = sacarGrupos(lisMain,llaves[i],start_index)
        lista_aux = lisMain[start_index : final_index+1]
        if len(lista_aux) == 1:
            # Si se recibe una lista de un solo elemento ya esta ordenada
            lista_ORD.append(lista_aux[0])
        else:
            if i + 1 < len(llaves):
                # Se ordena la sublista y se agrega al resultado
                lista_aux = sorted(lista_aux, key=lambda llave : llave[llaves[i+1]])
                #Parte Recursiva
                lista_aux = ordenarLista(lista_aux,llaves,i+1)
            for elem in lista_aux:
                lista_ORD.append(elem)
        start_index = final_index + 1
    return lista_ORD


def prepararExcel(main_df, lisMain):
    '''
        Funcion para preparar la salida de un Excel por medio de \n
        pandas.
        @main_df: Es un dataframe principal sin cambios de un Excel
        @lisMain: Es una lista de diccionarios de donde sacamos el orden
        @Return: Un diccionario con la estructura ordenada para main_df
    '''
    llaves = list(main_df)
    lista_Salida = []
    # Creamos listas para cada parte del diccionario del DataFrame
    for key in llaves:
        lista_aux = []
        for elem in lisMain:
            index = elem['indice']
            lista_aux.append(main_df[key][index])
        lista_Salida.append(lista_aux)
    lista_aux = []
    for elem in lisMain:
        clas = elem['clas']
        lista_aux.append(clas)
    lista_Salida.append(lista_aux)
    
    # Creamos el diccionario de Salida para Excel
    data_frame = {}
    for index in range(len(llaves)):
        data_frame[llaves[index]] = lista_Salida[index]
    data_frame['Final_Clasificación'] = lista_Salida[-1]
    return data_frame


def prepararErrorExcel(lisORD, lisDIC, lisNAME, txt_file):
    '''
        Función para ubicar libros erroneos
        @lisORD: Es una lista de diccionarios ya ordenada con los parametros
        @lisDIC: Es una lista de diccionarios que no esta ordenada
        @lisNAME: Es una lista que contiene todos los nombres de los libros
        @txt_file: Es un objeto para escribir en un archivo tipo txt
    '''
    lisSAL = []
    if len(lisORD) <= 5:
        txt_file.write('='*50 + '\n')
        txt_file.write("MUESTRA MUY PEQUEÑA DE LIBROS\n")
        txt_file.write("POR FAVOR INTERCALA MANUALMENTE\n")
        txt_file.write('='*50 + '\n')
        return

    # print('Lista de orden y diccionario iguales? ' + str(len(lisORD) == len(lisDIC)))
    if len(lisORD) == len(lisDIC):
        # txt_file.write("Empezando Organizador\n")
        # print("Comparando Indices de libros")
        # print("Izq = Entrada, Der= Salida")
        # print("++++++++++++++++++++++++++++++++")
        for ind in range(len(lisORD)):
            entry_INDX = lisDIC[ind]["indice"]
            out_INDX = lisORD[ind]["indice"]
            # print("Indices de DataFrame: " + str(entry_INDX) + "," + str(out_INDX))
            entry_clas = lisDIC[ind]["clas"]
            # entry_name = lisNAME[entry_INDX]
            if entry_INDX != out_INDX:
                # print("Clasificacion: \n" + entry_clas)
                # # out_clas = lisORD[ind]["clas"]
                # # print("Clasificacion: \n" + entry_clas + ' | ' + out_clas)
                
                # print("Nombre: \n" + STR_limit(entry_name, 25))
                # out_name = lisNAME[out_INDX]
                # print("Nombre: \n" + STR_limit(entry_name, 25) + ' | ' + STR_limit(out_name, 25))
                # Chequeo de Condicional o Completo Erroneo
                if (ind - 1) >= 0 or (ind + 1) < len(lisORD):
                    # text = "Erroneo"
                    cond = 0
                    if (ind - 1) >= 0: 
                        cond_INDX = lisORD[ind - 1]["indice"]
                        if entry_INDX == cond_INDX:
                            # text = "Condicional Anterior"
                            cond = -1
                    if (ind + 1) < len(lisORD):
                        cond_INDX = lisORD[ind + 1]["indice"]
                        if entry_INDX == cond_INDX:
                            # text = "Condicional Siguiente"
                            cond = 1
                    # print("Status: " + text)
                    lisSAL.append([entry_INDX, cond, entry_clas])
            else: 
                # print("Status: Correcto")
                lisSAL.append([entry_INDX, 2, entry_clas])
            # print("-"*70)
        # txt_file.write("\n")
        while True:
            cond_flag = False
            for index in range(len(lisSAL)):
                # Si el elemento es condicionado Anterior
                if lisSAL[index][1] == -1 and index - 1 >= 0 and lisSAL[index - 1][1] == 0:
                    lisCOPY = lisSAL[index - 1].copy()
                    lisSAL[index - 1] = lisSAL[index]
                    lisSAL[index - 1][1] = 2
                    
                    lisSAL[index] = lisCOPY
                    lisSAL[index][1] = 0
                    # Si el elemento es condicionado Siguiente
                if lisSAL[index][1] == 1 and index + 1 < len(lisSAL) and lisSAL[index + 1][1] == 0:
                    lisCOPY = lisSAL[index + 1].copy()
                    lisSAL[index + 1] = lisSAL[index]
                    lisSAL[index + 1][1] = 2

                    lisSAL[index] = lisCOPY
                    lisSAL[index][1] = 0
            
            for elem in lisSAL:
                # print(elem)
                if elem[1] == 1 or elem[1] == -1: cond_flag = True
            # print("==============")
            if not cond_flag: break

        lisERROR = []
        lisCORR = []
        for elem in lisSAL: 
            if elem[1] == 0: lisERROR.append(elem[0])
            else: lisCORR.append(elem[0])
        if lisERROR != []:
            error_Porcent = Porcent(len(lisERROR),len(lisDIC))
            txt_file.write('='*85 + '\n')
            txt_file.write("\tEL TOTAL: " + str(len(lisDIC)) + ", TIENES: " + str(len(lisERROR)) + ", QUE EQUIVALE AL: " + str(error_Porcent) +  "%\n")
            txt_file.write('='*85 + '\n')
            txt_file.write("\tPROCESO PARA ORGANIZAR LIBROS\n")
            txt_file.write("\tPASO 1. RETIRE LOS SIGUIENTES LIBROS\n")
            txt_file.write('='*85 + '\n')
            if len(lisERROR) < 20:
                if error_Porcent < 60:
                    # Proceso para retirar poco libros erroneos
                    for index in lisERROR:
                        for i in range(len(lisORD)):
                            if lisDIC[i]["indice"] == index:
                                txt_file.write('*'*85 + '\n')
                                txt_file.write("INFORMACION PARA RETIRAR\n")
                                x = i - 1
                                while x >= 0:
                                    # Poner Bandera AQUI
                                    if lisDIC[x]["indice"] in lisCORR:
                                        txt_file.write('Libro Anterior Correcto: ' + '| ' + lisDIC[x]["clas"] + ' | ' + STR_limit(lisNAME[lisDIC[x]["indice"]]['titulo']) + '\n')
                                        break
                                    x -= 1
                                txt_file.write('Seguido a este libro encontraras el libro que debes retirar:\n')
                                txt_file.write('Libro a Retirar: '+ '| ' + lisDIC[i]["clas"] + ' | ' + STR_limit(lisNAME[lisDIC[i]["indice"]]['titulo']) + '\n\n')
                                txt_file.write('*'*90 + '\n')
                else:
                    # Proceso para retirar muchos libros erroneos
                    for index in range(len(lisSAL)):
                        if lisSAL[index][1] == 0:
                            txt_file.write('*'*85 + '\n')
                            txt_file.write("INFORMACION PARA RETIRAR\n")
                            txt_file.write('Libro a retirar: '+ '| ' + lisORD[index]["clas"] + ' | ' + STR_limit(lisNAME[lisORD[index]["indice"]]['titulo']) + '\n\n')
                            txt_file.write('Este libro esta ubicado entre los siguientes libros correctos\n')
                            for x in range(len(lisSAL)):
                                if lisDIC[x]["indice"] == lisORD[index]["indice"]:
                                    pos_neg = x - 1
                                    pos_pos = x + 1
                                    while pos_neg >= 0:
                                        if lisDIC[pos_neg]["indice"] in lisCORR:
                                            txt_file.write('Libro Anterior Correcto:  ' + '| ' + lisDIC[pos_neg]["clas"] + ' | ' + STR_limit(lisNAME[lisDIC[pos_neg]["indice"]]['titulo']) + '\n')
                                            break
                                        pos_neg -= 1
                                    while pos_pos < len(lisORD):
                                        if lisDIC[pos_pos]["indice"] in lisCORR:
                                            txt_file.write('Libro Siguiente Correcto:  ' + '| ' + lisDIC[pos_pos]["clas"] + ' | ' + STR_limit(lisNAME[lisDIC[pos_pos]["indice"]]['titulo']) + '\n')
                                            break
                                        pos_pos += 1
                                    break
                            txt_file.write('*'*85 + '\n')
            else:
                # Proceso para retirar muchos libros erroneos
                for index in range(len(lisSAL)):
                    if lisSAL[index][1] == 0:
                        txt_file.write('*'*85 + '\n')
                        txt_file.write("INFORMACION PARA RETIRAR\n")
                        txt_file.write('Libro a retirar: '+ '| ' + lisORD[index]["clas"] + ' | ' + STR_limit(lisNAME[lisORD[index]["indice"]]['titulo']) + '\n\n')
                        txt_file.write('Este libro esta ubicado entre los siguientes libros correctos\n')
                        for x in range(len(lisSAL)):
                            if lisDIC[x]["indice"] == lisORD[index]["indice"]:
                                pos_neg = x - 1
                                pos_pos = x + 1
                                while pos_neg >= 0:
                                    if lisDIC[pos_neg]["indice"] in lisCORR:
                                        txt_file.write('Libro Anterior Correcto:  ' + '| ' + lisDIC[pos_neg]["clas"] + ' | ' + STR_limit(lisNAME[lisDIC[pos_neg]["indice"]]['titulo']) + '\n')
                                        break
                                    pos_neg -= 1
                                while pos_pos < len(lisORD):
                                    if lisDIC[pos_pos]["indice"] in lisCORR:
                                        txt_file.write('Libro Siguiente Correcto:  ' + '| ' + lisDIC[pos_pos]["clas"] + ' | ' + STR_limit(lisNAME[lisDIC[pos_pos]["indice"]]['titulo']) + '\n')
                                        break
                                    pos_pos += 1
                                break
                        txt_file.write('*'*85 + '\n')
            
            
            # txt_file.write('Erroneo' + ' | ' + elem[2] + ' | ' + STR_limit(lisNAME[elem[0]], 40))
            txt_file.write('\n\n\n')
            txt_file.write('='*90 + '\n')
            txt_file.write("\tPASO 2. INFORMACION PARA ACOMODAR LIBROS \n")
            txt_file.write('='*90 + '\n')
            # for elem in lisSAL: print(elem)
            # for elem in lisORD: print(elem["indice"]) 
            for index in range(len(lisSAL)):
                if lisSAL[index][1] == 0:
                    txt_file.write('+'*90 + '\n')
                    txt_file.write("INFORMACION PARA ACOMODAR\n")
                    pos_neg = index - 1
                    pos_pos = index + 1
                    ref = False
                    txt_file.write('Libro a Colocar: '+ '| ' + lisORD[index]["clas"] + ' | ' + STR_limit(lisNAME[lisORD[index]["indice"]]['titulo']) + '\n\n')
                    txt_file.write('Este libro va entre lo siguientes libros\n')
                    while pos_neg >= 0 and not ref:
                        if lisSAL[pos_neg][1] == 2:
                            txt_file.write('Libro Anterior:  ' + '| ' + lisORD[pos_neg]["clas"] + ' | ' + STR_limit(lisNAME[lisORD[pos_neg]["indice"]]['titulo']) + '\n')
                            # ref = True
                            break
                        pos_neg -= 1
                    while pos_pos < len(lisORD) and not ref:
                        if lisSAL[pos_pos][1] == 2:
                            txt_file.write('Libro Siguiente: ' + '| ' + lisORD[pos_pos]["clas"] + ' | ' + STR_limit(lisNAME[lisORD[pos_pos]["indice"]]['titulo']) + '\n')
                            # ref = True
                            break
                        pos_pos += 1
                    lisSAL[index][1] = 2
                    txt_file.write('+'*90 + '\n')
            txt_file.write('='*90 + '\n')
        else:
            txt_file.write('='*50 + '\n')
            txt_file.write("\t SIN CASOS PARA INTERCALAR\n")
            txt_file.write("LIBROS CORRECTAMENTE INTERCALAR\n")
            txt_file.write("FELICIDADES EL STAND ESTA CORRECTAMENTE INTERCALADO\n")
            txt_file.write('='*50 + '\n')
    else: print("Fallo en Intentar Organizar \n")


def escribirExcel(final_DF,key,writer):
    '''
        Funcion de Salida para escribir un Excel
        @nombre: Nombre del archivo final
        @path: Localidad donde se escribirá dicho archivo
        @dicc: Diccionario con estructura Data Frame para Excel
    '''
    df = pd.DataFrame(final_DF)
    llaves = list(df)
    df = df[llaves]
    df.to_excel(writer, sheet_name=key, index=False)


def imprimirResultados(CN,CLX,CMAT,CV,CE,CP,lenght,txt_file):
    '''
        Funcion para imprimir los resultados del analisis de cadenas \n
        Simplemente imprime de manera grafica los resultados
        @C1: Vector con valores para casos Normales
        @C2: Vector con valores para casos con Texto
        @C3: Vector con valores para casos con Versiones
        @C4: Valor de Casos Extranios
        @length: Recibe un valor int para comparar
    '''
    SumCN = CN + CLX
    SumCTMAT = CMAT
    SumCV = CV
    SumCE = CE
    SumCP = CP
    SumEnd = SumCN + SumCTMAT + SumCV + SumCE + SumCP
    txt_file.write('='*55 + '\n')
    txt_file.write("\t Detalle del Reporte \n")
    txt_file.write('='*55 + '\n')
    txt_file.write("Total de Casos Cargados: " + str(SumEnd) + '\n')
    txt_file.write("Casos Correctamente Analizados: " + str(SumEnd) + "\n")
    txt_file.write("Casos No Cargados: "+ str(lenght - SumEnd) + "\n")
    txt_file.write('='*55 + '\n')
    txt_file.write("Total de Items Analizados: " + str(SumEnd) + "/100%" + '\n')
    txt_file.write("Total de Items con Estandar LC Correcto: " + str(SumEnd - SumCE)+ "/" + str(Porcent((SumEnd - SumCE),SumEnd)) + '%\n')
    txt_file.write("Total de Items con Estandar LC Incorrecto: " + str(SumCE) + "/" + str(Porcent(SumCE,SumEnd)) + '%\n')
    txt_file.write('='*55 + '\n')
    txt_file.write("\n\n")

def imprimirLista(lisMain,STR,txt_file):
    '''
        Toma una lista e imprime los valores
    '''
    txt_file.write('='*85 + '\n')
    txt_file.write(STR + '\n')
    txt_file.write('='*85 + '\n')
    # llaves = list(lisMain[0])
    # for key in llaves:
    #         txt_file.write('|  ' + key[:4] + '  | ')
    txt_file.write('\n')
    for elem in lisMain:
        # txt_file.write(elem)
        llaves = list(elem)
        for key in llaves:
            txt_file.write('\t| ' + str(elem[key]))
        txt_file.write('\n')
    txt_file.write('='*85 + '\n')


if __name__ == '__main__':
    Nombre = "C:\\00_UniversidadTec\\09 SextSemestre22\\01_SB\Excel\Prueba1_9-03-2022.xlsx"
    pagina = "" 
    print(cargarDatos(Nombre))