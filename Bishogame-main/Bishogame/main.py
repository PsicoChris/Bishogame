# main.py - El punto de entrada principal del juego

import pygame
import sys

from config import ANCHO, ALTO # Asegúrate de que ANCHO y ALTO se importen
from menu_screen import mostrar_menu_principal
from highscores_screen import mostrar_puntuaciones_maximas
from game_screen import run_game
from score_manager import guardar_puntuacion

def main():
    pygame.init()
    # ¡CAMBIO! La ventana se crea con las nuevas dimensiones de config
    ventana = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("BishoGame")

    reloj = pygame.time.Clock()

    estado_juego = "menu"

    while True:
        if estado_juego == "menu":
            opcion_menu = mostrar_menu_principal(ventana, reloj)
            if opcion_menu == "jugar":
                estado_juego = "jugar"
            elif opcion_menu == "puntuaciones":
                estado_juego = "puntuaciones"
        elif estado_juego == "puntuaciones":
            mostrar_puntuaciones_maximas(ventana, reloj)
            estado_juego = "menu"
        elif estado_juego == "jugar":
            puntuacion_final, jugador_gano = run_game(ventana, reloj)
            guardar_puntuacion(puntuacion_final)
            estado_juego = "menu"

if __name__ == '__main__':
    main()