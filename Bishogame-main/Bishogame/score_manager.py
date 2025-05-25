# score_manager.py - Gestiona la carga y guardado de puntuaciones máximas

import os
from config import ARCHIVO_PUNTUACIONES, MAX_PUNTUACIONES

def cargar_puntuaciones():
    """Carga las puntuaciones desde el archivo, las ordena y devuelve el top X."""
    puntuaciones = []
    if os.path.exists(ARCHIVO_PUNTUACIONES):
        with open(ARCHIVO_PUNTUACIONES, 'r') as f:
            for line in f:
                try:
                    puntuaciones.append(int(line.strip()))
                except ValueError:
                    continue # Ignora líneas inválidas
    puntuaciones.sort(reverse=True) # Ordenar de mayor a menor
    return puntuaciones[:MAX_PUNTUACIONES] # Devolver solo el top X

def guardar_puntuacion(nueva_puntuacion):
    """Añade una nueva puntuación, reordena y guarda el top X en el archivo."""
    puntuaciones = cargar_puntuaciones()
    puntuaciones.append(nueva_puntuacion)
    puntuaciones.sort(reverse=True)
    puntuaciones = puntuaciones[:MAX_PUNTUACIONES] # Mantener solo el top X

    with open(ARCHIVO_PUNTUACIONES, 'w') as f:
        for score in puntuaciones:
            f.write(f"{score}\n")