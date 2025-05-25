# config.py - Contiene todas las constantes globales

import pygame

# --- Dimensiones de la Ventana (¡CAMBIADO!) ---
ANCHO = 1024 # Aumentado de 850
ALTO = 600   # Aumentado de 480

# --- Colores (RGB) ---
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
GRIS_OSCURO = (120, 100, 40)
VERDE_PUNTOS = (0, 200, 0)
AZUL_CLARO = (173, 216, 230)
GRIS_CLARO = (200, 200, 200)
GRIS_TRANSPARENTE = (0, 0, 0, 150)

# --- Velocidades ---
VELOCIDAD_JUGADOR = 15
VELOCIDAD_BALON_JUGADOR = 10
VELOCIDAD_BALON_ENEMIGO = 3   # ¡CAMBIADO! De 5 a 3 (más lento)
VELOCIDAD_ENEMIGO_MOV = 2
DESPLAZAMIENTO_VERTICAL_ENEMIGO = 40

# --- Rutas de Imágenes ---
IMAGEN_BISHO = 'imgsonly/bisho.png'
IMAGEN_BALON_JUGADOR = 'imgsonly/ball.png'
IMAGEN_DISPARO_ENEMIGO = 'imgsonly/nouu.png'
IMAGEN_FONDO = 'imgsonly/estadio.jpg'

# --- Configuración de Enemigos (¡CAMBIADO!) ---
ENEMIGO_TIPOS = [
    # Nueva estructura: 'escala' para ajustar el tamaño de la imagen
    {'img1': 'imgsonly/ballgold.png', 'img2': 'imgsonly/nocr01.png', 'y_offset': 100, 'puntos': 10, 'escala': 0.7}, # Más pequeños
    {'img1': 'imgsonly/agua.png', 'img2': 'imgsonly/coca.png', 'y_offset': 0, 'puntos': 20, 'escala': 0.7},
    {'img1': 'imgsonly/canchis.png', 'img2': 'imgsonly/canchis2.png', 'y_offset': -100, 'puntos': 30, 'escala': 0.7},
]
ENEMIGOS_POR_FILA = 6 # ¡CAMBIADO! De 4 a 6

# --- Configuración de Puntuaciones ---
ARCHIVO_PUNTUACIONES = 'puntuaciones.txt'
MAX_PUNTUACIONES = 5

# --- Teclas de Control ---
TECLA_PAUSA = pygame.K_ESCAPE

# --- Frecuencia de Disparo Enemigo (¡NUEVO!) ---
FRECUENCIA_DISPARO_ENEMIGO = 98 # % probabilidad de NO disparar. 98 significa 2% de chance de disparar.
                               # Un valor más alto hace que disparen MENOS FRECUENTE.
                               # Antes, era un valor bajo (ej. 1), ahora lo invertimos para ser más claro.

# --- Fuentes ---
FUENTE_FIN_JUEGO_TAM = 50
FUENTE_PUNTUACION_TAM = 30
FUENTE_MENU_TITULO_TAM = 70
FUENTE_MENU_BOTON_TAM = 40
FUENTE_PUNT_MAX_TITULO_TAM = 60
FUENTE_PUNT_MAX_PUNT_TAM = 35
FUENTE_PUNT_MAX_VOLVER_TAM = 30
FUENTE_PAUSA_TITULO_TAM = 60
FUENTE_PAUSA_BOTON_TAM = 40