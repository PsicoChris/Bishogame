# highscores_screen.py - Pantalla de puntuaciones máximas

import pygame
import sys
from config import ANCHO, ALTO, BLANCO, AZUL_CLARO, GRIS_CLARO, IMAGEN_FONDO
from config import FUENTE_PUNT_MAX_TITULO_TAM, FUENTE_PUNT_MAX_PUNT_TAM, FUENTE_PUNT_MAX_VOLVER_TAM
from utils import dibujar_texto, dibujar_boton
from score_manager import cargar_puntuaciones

def mostrar_puntuaciones_maximas(ventana, reloj):
    """Muestra la lista de puntuaciones máximas."""
    fuente_titulo = pygame.font.SysFont("Times New Roman", FUENTE_PUNT_MAX_TITULO_TAM)
    fuente_puntuacion = pygame.font.SysFont("Times New Roman", FUENTE_PUNT_MAX_PUNT_TAM)
    fuente_volver = pygame.font.SysFont("Times New Roman", FUENTE_PUNT_MAX_VOLVER_TAM)

    puntuaciones = cargar_puntuaciones()

    boton_volver_rect = pygame.Rect(ANCHO // 2 - 75, ALTO - 100, 150, 60)

    # Cargar el fondo de puntuaciones una sola vez
    try:
        fondo_puntuaciones = pygame.image.load(IMAGEN_FONDO).convert()
    except pygame.error as e:
        print(f"Error al cargar la imagen de fondo de puntuaciones ({IMAGEN_FONDO}): {e}")
        pygame.quit()
        sys.exit()

    while True:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if boton_volver_rect.collidepoint(mouse_pos):
                    return # Volver al menú principal

        ventana.blit(fondo_puntuaciones, (0, 0))

        dibujar_texto(ventana, "Puntuaciones Máximas", fuente_titulo, BLANCO, ANCHO // 2, 80)

        y_offset = 180
        if not puntuaciones:
            dibujar_texto(ventana, "No hay puntuaciones aún.", fuente_puntuacion, BLANCO, ANCHO // 2, y_offset)
        else:
            for i, score in enumerate(puntuaciones):
                dibujar_texto(ventana, f"{i+1}. {score}", fuente_puntuacion, BLANCO, ANCHO // 2, y_offset + i * 40)

        dibujar_boton(ventana, boton_volver_rect, "Volver", fuente_volver, AZUL_CLARO, GRIS_CLARO, mouse_pos)

        pygame.display.flip()
        reloj.tick(60)