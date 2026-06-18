import numpy as np

# Configuración del Alfabeto Español (27 letras)
ALFABETO = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"
MAPA_L_N = {l: i for i, l in enumerate(ALFABETO)}
MAPA_N_L = {i: l for i, l in enumerate(ALFABETO)}

# Matriz de Hill 2x2 definida por el usuario
MATRIZ_HILL = np.array([[3, 2], [1, 1]])

def cifrar_hill(texto):
    # Limpiar texto
    texto = "".join([c for c in texto.upper() if c in ALFABETO])
    # Relleno si es impar
    if len(texto) % 2 != 0: 
        texto += "X"
    
    nums = [MAPA_L_N[c] for c in texto]
    resultado = ""
    
    # Procesar bloques de 2
    for i in range(0, len(nums), 2):
        vector = np.array([nums[i], nums[i+1]])
        cifrado = np.dot(MATRIZ_HILL, vector) % 27
        resultado += MAPA_N_L[cifrado[0]] + MAPA_N_L[cifrado[1]]
    
    return resultado

def aplicar_cesar_y_metadato(cifrado):
    longitud = len(cifrado)
    
    # Buscar duplicados para aplicar la "Regla Enigma"
    for i, letra in enumerate(cifrado):
        if cifrado.count(letra) > 1:
            # Aplicar César selectivo
            nueva_idx = (MAPA_L_N[letra] + longitud) % 27
            nueva_letra = MAPA_N_L[nueva_idx]
            # Reemplazar solo la primera ocurrencia
            cifrado_final = cifrado[:i] + nueva_letra + cifrado[i+1:]
            return cifrado_final, longitud, letra
            
    return cifrado, None, None
