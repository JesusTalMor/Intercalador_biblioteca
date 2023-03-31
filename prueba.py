alphabet = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
STR = 'PQ7298.424.A76 .O744 2007'
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
