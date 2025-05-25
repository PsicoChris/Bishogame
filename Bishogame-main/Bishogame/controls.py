# controls.py - Maneja la entrada del usuario (teclado y ratón)

import pygame
import sys
from pygame.locals import *
from config import TECLA_PAUSA


def handle_input(event, jugador, player_bullets, all_sprites, current_game_state_in_run_game):
    """
    Procesa un evento de Pygame y actualiza el estado del juego o los sprites.

    Args:
        event (pygame.event.Event): El evento actual de Pygame.
        jugador (BishoSiu): Instancia del jugador.
        player_bullets (pygame.sprite.Group): Grupo de balas del jugador.
        all_sprites (pygame.sprite.Group): Grupo de todos los sprites.
        current_game_state_in_run_game (str): El estado actual dentro de run_game
                                               ("running" o "paused").

    Returns:
        str: Un comando de control para game_screen.py (ej. "PAUSE", "UNPAUSE", "QUIT"),
             o None si el evento es procesado internamente o no requiere un cambio de estado.
    """
    if event.type == QUIT:
        return "QUIT"

    if current_game_state_in_run_game == "running":
        if event.type == KEYDOWN:
            if event.key == K_LEFT:
                jugador.movIzq()  # Establece la bandera de movimiento
            elif event.key == K_RIGHT:
                jugador.movDer()  # Establece la bandera de movimiento
            elif event.key == K_c:
                nuevo_balon = jugador.cabecear()
                if nuevo_balon:
                    all_sprites.add(nuevo_balon)
                    player_bullets.add(nuevo_balon)
            elif event.key == TECLA_PAUSA:
                return "PAUSE"
        # ¡NUEVO! Manejar KEYUP para detener el movimiento
        elif event.type == KEYUP:
            if event.key == K_LEFT:
                jugador.detener_movimiento("izquierda")
            elif event.key == K_RIGHT:
                jugador.detener_movimiento("derecha")

    elif current_game_state_in_run_game == "paused":
        if event.type == KEYDOWN:
            if event.key == TECLA_PAUSA:
                return "UNPAUSE"

    return None