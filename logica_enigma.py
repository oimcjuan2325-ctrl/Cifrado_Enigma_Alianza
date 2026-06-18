import numpy as np

# Configuración: Alfabeto de 27 letras (A-Z + Ñ)
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

def descifrar_hill(texto_cifrado):
    # Determinante = (3*1 - 2*1) = 1. Inversa módulo 27 es ella misma.
    # Matriz inversa: [[1, -2], [-1, 3]] -> Mod 27: [[1, 25], [26, 3]]
    inv_matriz = np.array([[1, 25], [26, 3]])
    nums = [MAPA_L_N[c] for c in texto_cifrado.upper()]
    resultado = ""
    for i in range(0, len(nums), 2):
        vector = np.array([nums[i], nums[i+1]])
        descifrado = np.dot(inv_matriz, vector) % 27
        resultado += MAPA_N_L[descifrado[0]] + MAPA_N_L[descifrado[1]]
    return resultado.replace("X", "")
