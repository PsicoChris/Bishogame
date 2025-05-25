# menu_screen.py - Pantalla del menú principal

import pygame
import sys
from config import ANCHO, ALTO, BLANCO, AZUL_CLARO, GRIS_CLARO, IMAGEN_FONDO
from config import FUENTE_MENU_TITULO_TAM, FUENTE_MENU_BOTON_TAM
from utils import dibujar_texto, dibujar_boton

def mostrar_menu_principal(ventana, reloj):
    """Muestra el menú principal y espera la interacción del usuario."""
    fuente_titulo = pygame.font.SysFont("Times New Roman", FUENTE_MENU_TITULO_TAM)
    fuente_boton = pygame.font.SysFont("Times New Roman", FUENTE_MENU_BOTON_TAM)

    # Definir rectángulos para los botones
    boton_jugar_rect = pygame.Rect(ANCHO // 2 - 100, ALTO // 2 - 50, 200, 70)
    boton_puntuaciones_rect = pygame.Rect(ANCHO // 2 - 150, ALTO // 2 + 50, 300, 70)
    boton_salir_rect = pygame.Rect(ANCHO // 2 - 75, ALTO // 2 + 150, 150, 70)

    # Cargar el fondo del menú una sola vez
    try:
        fondo_menu = pygame.image.load(IMAGEN_FONDO).convert()
    except pygame.error as e:
        print(f"Error al cargar la imagen de fondo del menú ({IMAGEN_FONDO}): {e}")
        pygame.quit()
        sys.exit()

    while True:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if boton_jugar_rect.collidepoint(mouse_pos):
                    return "jugar"
                if boton_puntuaciones_rect.collidepoint(mouse_pos):
                    return "puntuaciones"
                if boton_salir_rect.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()

        ventana.blit(fondo_menu, (0, 0))

        dibujar_texto(ventana, "BishoGame", fuente_titulo, BLANCO, ANCHO // 2, ALTO // 4)

        dibujar_boton(ventana, boton_jugar_rect, "Jugar", fuente_boton, AZUL_CLARO, GRIS_CLARO, mouse_pos)
        dibujar_boton(ventana, boton_puntuaciones_rect, "Puntuaciones Máximas", fuente_boton, AZUL_CLARO, GRIS_CLARO, mouse_pos)
        dibujar_boton(ventana, boton_salir_rect, "Salir", fuente_boton, AZUL_CLARO, GRIS_CLARO, mouse_pos)

        pygame.display.flip()
        reloj.tick(60)