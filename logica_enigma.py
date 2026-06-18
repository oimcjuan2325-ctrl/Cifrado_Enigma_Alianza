import numpy as np

# Alfabeto de 27 caracteres (A-Z + Ñ)
ALFABETO = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"
MAPA_L_N = {l: i for i, l in enumerate(ALFABETO)}
MAPA_N_L = {i: l for i, l in enumerate(ALFABETO)}
MATRIZ_HILL = np.array([[3, 2], [1, 1]])

def cifrar_hill(texto):
    texto = "".join([c for c in texto.upper() if c in ALFABETO])
    if len(texto) % 2 != 0: texto += "X"
    
    nums = [MAPA_L_N[c] for c in texto]
    resultado = ""
    
    for i in range(0, len(nums), 2):
        vector = np.array([nums[i], nums[i+1]])
        cifrado = np.dot(MATRIZ_HILL, vector) % 27
        resultado += MAPA_N_L[cifrado[0]] + MAPA_N_L[cifrado[1]]
    return resultado

def aplicar_cesar_y_metadato(cifrado):
    # Detecta repetición (si hay letras iguales consecutivas o totales)
    # Aplicamos César basado en la longitud total del texto cifrado
    longitud = len(cifrado)
    
    # Buscamos la primera letra que se repite
    for i, letra in enumerate(cifrado):
        if cifrado.count(letra) > 1:
            # Aplicamos César a esa letra específica
            nueva_letra_idx = (MAPA_L_N[letra] + longitud) % 27
            nueva_letra = MAPA_N_L[nueva_letra_idx]
            cifrado_final = cifrado[:i] + nueva_letra + cifrado[i+1:]
            return cifrado_final, longitud, letra
            
    return cifrado, None, None
