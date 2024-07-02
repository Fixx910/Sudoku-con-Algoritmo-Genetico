import numpy as np
import random
import matplotlib.pyplot as plt

def inicializarIndividuo(plantilla):
    """ Inicializa un individuo basado en una plantilla dada.
        Rellena los ceros con números aleatorios del 1 al 9 sin repetir en cada fila."""
    individuo = np.array(plantilla, dtype=int).copy()
    
    for fila in range(9):
        # Encontrar los números que ya están en la fila
        existentes = set(individuo[fila]) - {0}
        # Encontrar los números que faltan en la fila
        faltantes = list(set(range(1, 10)) - existentes)
        random.shuffle(faltantes)
        
        # Rellenar los ceros con los números faltantes
        idx = 0
        for col in range(9):
            if individuo[fila][col] == 0:
                individuo[fila][col] = faltantes[idx]
                idx += 1
    
    return individuo

def inicializarPoblacion(plantilla, tamanPoblacion):
    """ Inicializa una población de Sudokus basada en una plantilla dada."""
    poblacion = [inicializarIndividuo(plantilla) for _ in range(tamanPoblacion)]
    return poblacion

def contarRepetidos(lista):
    """ Cuenta los números repetidos en una lista de 9 elementos."""
    repetidos = 0
    contador = [0] * 10  # Cada elemento asume el conteo de los números del 1 al 9
    for num in lista:
        if num != 0:
            contador[num] += 1
            if contador[num] > 1:
                repetidos += 1
    return repetidos

def funcionObjetivo(sudoku):
    """ Calcula la función objetivo para un Sudoku 9x9.
        Cuenta el total de números repetidos en filas, columnas y regiones 3x3."""
    repetidos_totales = 0
    
    # Repeticiones en filas
    for fila in sudoku:
        repetidos_totales += contarRepetidos(fila)
    
    # Repeticiones en columnas
    for col in range(9):
        columna = [sudoku[fila][col] for fila in range(9)]
        repetidos_totales += contarRepetidos(columna)
    
    # Repeticiones en regiones 3x3
    for i in range(3):
        for j in range(3):
            region = []
            for k in range(3):
                for l in range(3):
                    region.append(sudoku[i*3+k][j*3+l])
            repetidos_totales += contarRepetidos(region)
    
    return repetidos_totales

def cruza1Punto(padre1, padre2):
    """ Realiza la cruza de dos individuos (padres) para producir dos hijos.
        Cada hijo toma algunas filas de un padre y otras filas del otro padre. """
    hijo1 = np.zeros((9, 9), dtype=int)
    hijo2 = np.zeros((9, 9), dtype=int)
    
    # Generar un punto de cruza
    punto_cruza = random.randint(1, 8)  # Elegir un punto de cruza entre 1 y 8
    
    # Crear el primer hijo
    hijo1[:punto_cruza] = padre1[:punto_cruza]
    hijo1[punto_cruza:] = padre2[punto_cruza:]
    
    # Crear el segundo hijo
    hijo2[:punto_cruza] = padre2[:punto_cruza]
    hijo2[punto_cruza:] = padre1[punto_cruza:]
    
    return hijo1, hijo2

def cruzaPorFilas(padre1, padre2, rowCrossverRate=0.7):
    """ Realiza la cruza de dos individuos (padres) para producir dos hijos.
        Se recorre cada fila de los padres y se genera un número random, si el número
        es mayor al umbral, la fila se intercambia. """
    hijo1 = np.array(padre1, dtype=int).copy()
    hijo2 = np.array(padre2, dtype=int).copy()
    
    for fila in range(9):
        if  random.random() > rowCrossverRate:
            # Intercambiar la fila entre los dos hijos
            hijo1[fila], hijo2[fila] = hijo2[fila].copy(), hijo1[fila].copy()
    
    return hijo1, hijo2

def mutacionIntercambio(individuo, plantilla, swapMutationRate=0.8):
    """ Realiza la mutación de un individuo.
    Intercambia dos números al azar en una fila con una probabilidad dada,
    asegurando no modificar las celdas fijas de la plantilla. """
    for fila in range(9):
        if random.random() < swapMutationRate:
            # Encuentra las columnas que no son fijas en una fila random
            columnas = [col for col in range(9) if plantilla[fila][col] == 0]
            if len(columnas) > 1:
                col1, col2 = random.sample(columnas, 2)
                individuo[fila][col1], individuo[fila][col2] = individuo[fila][col2], individuo[fila][col1]
    return individuo

def reinicializarFila(fila, plantilla_fila):
    """ Inicializa una fila del Sudoku basada en una plantilla dada.
        Rellena los ceros con números aleatorios del 1 al 9 sin repetir. """
    individuo_fila = np.array(fila, dtype=int).copy()
    
    # Encontrar los números que ya están en la fila
    existentes = set(individuo_fila) - {0}
    # Encontrar los números que faltan en la fila
    faltantes = list(set(range(1, 10)) - existentes)
    random.shuffle(faltantes)
    
    # Rellenar los ceros con los números faltantes
    idx = 0
    for col in range(9):
        if plantilla_fila[col] == 0:
            individuo_fila[col] = faltantes[idx]
            idx += 1
    
    return individuo_fila

def mutacionReinicializacion(individuo, plantilla, reinitializationMutationRate=0.4):
    """ Realiza la mutación de reinicialización de filas en un individuo.
        Si el número random es menor a un umbral, reinicializa todos los elementos
        de esa fila excepto los números fijos. """
    for fila in range(9):
        if random.random() < reinitializationMutationRate:
            individuo[fila] = reinicializarFila(individuo[fila], plantilla[fila])
    return individuo

def encontrarIndicesRepetidos(lista):
    indice_por_valor = {}
    for indice, valor in enumerate(lista):
        if valor in indice_por_valor:
            return [indice_por_valor[valor], indice]
        else:
            indice_por_valor[valor] = indice
    return None 

def encontrarColumnasIlegales(individuo):
    """ Encuentra las columnas ilegales (con números repetidos) en un Sudoku. """
    columnas_ilegales = []
    for col in range(9):
        columna = individuo[:, col]
        if len(columna) != len(set(columna)):  # Hay números repetidos
            columnas_ilegales.append([col, encontrarIndicesRepetidos(columna)])
    return columnas_ilegales

def busquedaLocal(individuo):
    columnasIlegales = encontrarColumnasIlegales(individuo)
    individuoColumnas = [list(col) for col in zip(*individuo)]
    plantilla = individuo.copy()  # Guardar la plantilla original

    for i, dupla in enumerate(columnasIlegales):
        if i == len(columnasIlegales) - 1:
            break
        for j in range(2):
            for k in range(2):
                col1, idx1 = dupla[0], dupla[1][j]
                col2, idx2 = columnasIlegales[i + 1][0], columnasIlegales[i + 1][1][k]
                
                if plantilla[idx1][col1] == 0 and plantilla[idx2][col2] == 0:
                    if dupla[1][j] == columnasIlegales[i + 1][1][k]:
                        individuoColumnas[col1][dupla[1][j]], individuoColumnas[col2][columnasIlegales[i + 1][1][k]] = individuoColumnas[col2][columnasIlegales[i + 1][1][k]], individuoColumnas[col1][dupla[1][j]]

    individuo = np.array([list(row) for row in zip(*individuoColumnas)], dtype=int)

    return individuo

#---------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------

def calculaAptitudes(poblacion, funcion):

	aptitudes = []

	for individuo in poblacion:

		aptitudes.append(funcion(individuo))

	return aptitudes

#---------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------

def seleccionPadres(poblacion, aptitudes, metodoReproduccion, minOmax = 'min'):

  seleccionados = []

  individuos = list(zip(poblacion, aptitudes))

  while len(seleccionados) < len(poblacion):
    padre1 = metodoReproduccion(individuos, minOmax)
    padre2 = metodoReproduccion(individuos, minOmax)

    while np.array_equal(padre1, padre2):
      # print(f'El padre 1: {padre1} es igual a padre 2: {padre2}')
      padre2 = metodoReproduccion(individuos, minOmax)
      # print(f'El padre 2 ha sido reasignado como: {padre2}\n')

    seleccionados += [padre1, padre2]

  return seleccionados

#---------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------

def torneo(individuos, minOmax = 'min'):

  participantes = random.sample(individuos, 2)
  if minOmax == 'min':
    ganador = min(participantes, key = lambda x: x[1])
  else:
    ganador = max(participantes, key = lambda x: x[1])
  return ganador[0]

#---------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------

def reproduccion(sudoku, padres, metodoReproduccion, metodoMutacion, crossoverRate, mutacionRate):

    if len(padres) % 2 == 1:
        padres.pop()

    descendencia = []

    for i in range(0, len(padres), 2):
        if random.uniform(0, 1) <= crossoverRate:
          # print('Se estan cruzando')
          hijos = metodoReproduccion(padres[i], padres[i+1])
          descendencia.append(hijos[0])
          descendencia.append(hijos[1])

          # print(f'Los hijos de {padres[i]} con {padres[i+1]} son\n{hijos[0]}\n{hijos[1]}')

    for i in range(len(descendencia)):
        if random.uniform(0, 1) <= mutacionRate:
            descendencia[i] = metodoMutacion(descendencia[i], sudoku, 0.5)

    return descendencia

#---------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------

def seleccionSobrevivientes(padres, descendientes, cantidadSobrevivientes, funcion, minOmax = 'min'):

  poblacion = padres + descendientes

  if minOmax == 'min':
    poblacion = sorted(poblacion, key = lambda x: funcion(x))
  else:
    poblacion = sorted(poblacion, key = lambda x: funcion(x), reverse = True)

  poblacion = poblacion[:cantidadSobrevivientes]

  return poblacion

def matrizATupla(matriz):
  return tuple(tuple(fila) for fila in matriz)

def aprendizajePoblacionElite(poblacion, descendientes, cantidadSobrevivientes, funcion, minOmax = 'min'):

  poblacion = seleccionSobrevivientes(poblacion, descendientes, cantidadSobrevivientes, funcion, minOmax)

#---------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------

def algoritmoGeneticoPermutaciones(sudoku, funcion, poblacion, generacionesTotales, metodoSeleccion, crossoverRate, mutationRate):
  print('Creando la primera generacion:\n')

  generacion = 0
  valoresOptimos = []
  numeroPoblacion = len(poblacion)

  for i in range(generacionesTotales):

    generacion += 1
    print(f'\nGeneracion {generacion}\n')

    aptitudes = calculaAptitudes(poblacion, funcion)

    padres = seleccionPadres(poblacion, aptitudes, metodoSeleccion)

    hijos = reproduccion(sudoku, padres, cruzaPorFilas, mutacionIntercambio, crossoverRate, mutationRate)

    aptitudesHijos = calculaAptitudes(hijos, funcion)

    aux = poblacion + hijos
    poblacion = []

    # Usamos un conjunto para llevar un seguimiento de las matrices ya vistas
    matrices_vistas = set()

    for i in aux:
        # Convertimos la matriz a una representación inmutable (tupla de tuplas)
        matriz_tupla = matrizATupla(i)
        if matriz_tupla not in matrices_vistas:
            poblacion.append(i)
            matrices_vistas.add(matriz_tupla)

    aptitudes = calculaAptitudes(poblacion, funcion)

    poblacion = sorted(poblacion, key = lambda x: funcion(x))
    poblacion = poblacion[:numeroPoblacion]

    #----------------------------------------------------

    aux = []
    for i in range(len(poblacion)):
      aux.append(busquedaLocal(poblacion[i]))

    poblacion = aux

    aptitudes = calculaAptitudes(poblacion, funcion)

    poblacion = sorted(poblacion, key = lambda x: funcion(x))
    poblacion = poblacion[:numeroPoblacion]

    #----------------------------------------------------

    valoresOptimos.append(funcion(poblacion[0]))

    print(f'Individuo optimo:')
    print(poblacion[0])
    aptitud = funcion(poblacion[0])
    print(f'\n\tSu aptitud es de {funcion(poblacion[0])}')

    if aptitud == 0:
      break

  return poblacion[0]
#   plt.plot(range(1, generacion+1), valoresOptimos)
#   plt.xlabel('Número de Generación')
#   plt.ylabel('Valor Óptimo')
#   plt.title('Valor Óptimo en Cada Generación')
#   plt.grid(True)
#   plt.show()

if __name__ == '__main__':

    sudoku = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 5, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ]

    tamanoPoblacion = 100
    generacionesTotales = 500

    cantidadPadres = 100
    cantidadSobrevivientes = tamanoPoblacion

    crossoverRate = 0.9
    mutationRate = 0.4
    rowCrossoverRate = 0.1
    swapMutationRate = 0.2
    reinitializationMutationRate = 0.2

    funcion = funcionObjetivo

    poblacion = inicializarPoblacion(sudoku, tamanoPoblacion)
    algoritmoGeneticoPermutaciones(sudoku, funcion, poblacion, generacionesTotales, torneo, crossoverRate, mutationRate)