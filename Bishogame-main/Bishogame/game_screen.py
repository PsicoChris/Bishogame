# game_screen.py - Contiene la lógica principal del juego

import pygame
import sys
from random import randint

from config import ANCHO, ALTO, ENEMIGO_TIPOS, GRIS_OSCURO, VERDE_PUNTOS, BLANCO, AZUL_CLARO, GRIS_CLARO, \
    GRIS_TRANSPARENTE, IMAGEN_FONDO
from config import FUENTE_FIN_JUEGO_TAM, FUENTE_PUNTUACION_TAM, FUENTE_PAUSA_TITULO_TAM, FUENTE_PAUSA_BOTON_TAM
from config import ENEMIGOS_POR_FILA  # ¡NUEVA IMPORTACIÓN! Para el número de enemigos por fila
from player import BishoSiu
from enemy import noCreyente
from bullet import Balon
from score_manager import guardar_puntuacion
from utils import dibujar_texto, dibujar_boton
from controls import handle_input


def cargar_enemigos_para_juego(enemy_group, all_sprites, jugador_sprite):
    """
    Carga los enemigos en sus respectivos grupos para una nueva partida.
    Asegura que el jugador esté en all_sprites.
    """
    enemy_group.empty()

    if jugador_sprite not in all_sprites:
        all_sprites.add(jugador_sprite)

    # Calcular el espaciado horizontal para los nuevos ANCHO y ENEMIGOS_POR_FILA
    espacio_entre_enemigos = ANCHO // (ENEMIGOS_POR_FILA + 1)

    # Crear dos filas de enemigos de cada tipo para que haya más en el campo de juego
    y_offsets = [100, 150]  # Un poco más bajo para la segunda fila

    for fila_idx, y_offset_base in enumerate(y_offsets):
        for tipo_enemigo_idx, tipo_enemigo in enumerate(ENEMIGO_TIPOS):
            # Calcular la posición Y del enemigo, ajustando por fila y tipo
            # Esto hará que los enemigos se escalonen verticalmente en el campo de juego
            pos_y = y_offset_base + tipo_enemigo['y_offset']

            for i in range(ENEMIGOS_POR_FILA):  # ¡CAMBIO! Usamos ENEMIGOS_POR_FILA
                posx = espacio_entre_enemigos * (i + 1)

                enemigo = noCreyente(posx, pos_y, 40,
                                     tipo_enemigo['img1'], tipo_enemigo['img2'],
                                     tipo_enemigo['puntos'], tipo_enemigo['escala'])  # ¡CAMBIO! Pasamos la escala
                enemy_group.add(enemigo)
                all_sprites.add(enemigo)


def run_game(ventana, reloj):
    """
    Contiene el bucle principal del juego.
    Retorna la puntuación final y si el jugador ganó.
    """
    # Establecer el tamaño de la ventana al inicio de la función del juego
    # Esto es redundante si ya lo haces en main.py, pero asegura que sea el correcto
    # (Ya lo haces en main.py, así que esto es más un recordatorio de que debe ser así)
    # ventana = pygame.display.set_mode((ANCHO, ALTO)) # ¡No descomentar! Ya está hecho en main.py

    fuente_fin_juego = pygame.font.SysFont("Times New Roman", FUENTE_FIN_JUEGO_TAM)
    fuente_puntuacion = pygame.font.SysFont("Times New Roman", FUENTE_PUNTUACION_TAM)

    fuente_pausa_titulo = pygame.font.SysFont("Times New Roman", FUENTE_PAUSA_TITULO_TAM)
    fuente_pausa_boton = pygame.font.SysFont("Times New Roman", FUENTE_PAUSA_BOTON_TAM)

    try:
        fondoimagen = pygame.image.load(IMAGEN_FONDO).convert()
        # Escalar el fondo para que coincida con el nuevo tamaño de la ventana
        fondoimagen = pygame.transform.scale(fondoimagen, (ANCHO, ALTO))  # ¡NUEVO! Escalar el fondo
    except pygame.error as e:
        print(f"Error al cargar la imagen de fondo del juego ({IMAGEN_FONDO}): {e}")
        pygame.quit()
        sys.exit()

    all_sprites = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    enemy_group = pygame.sprite.Group()
    player_bullets = pygame.sprite.Group()
    enemy_bullets = pygame.sprite.Group()

    jugador = BishoSiu()
    all_sprites.add(jugador)
    player_group.add(jugador)

    player_bullets.empty()
    enemy_bullets.empty()
    cargar_enemigos_para_juego(enemy_group, all_sprites, jugador)

    puntuacion = 0
    en_juego = True
    pausado = False

    boton_reanudar_rect = pygame.Rect(ANCHO // 2 - 100, ALTO // 2 - 50, 200, 70)
    boton_menu_principal_rect = pygame.Rect(ANCHO // 2 - 150, ALTO // 2 + 50, 300, 70)

    while en_juego:
        current_time = pygame.time.get_ticks()
        reloj.tick(60)

        for event in pygame.event.get():
            command = handle_input(event, jugador, player_bullets, all_sprites, "paused" if pausado else "running")

            if command == "QUIT":
                pygame.quit()
                sys.exit()
            elif command == "PAUSE":
                pausado = True
            elif command == "UNPAUSE":
                pausado = False

            if pausado and event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if boton_reanudar_rect.collidepoint(mouse_pos):
                    pausado = False
                elif boton_menu_principal_rect.collidepoint(mouse_pos):
                    guardar_puntuacion(puntuacion)
                    return puntuacion, jugador.vida

        if not pausado:
            if not jugador.vida:
                en_juego = False
                continue

            all_sprites.update(current_time)

            for enemigo in enemy_group:
                disparo = enemigo.atacar()
                if disparo:
                    all_sprites.add(disparo)
                    enemy_bullets.add(disparo)

            hits_player_bullet_enemy = pygame.sprite.groupcollide(enemy_group, player_bullets, True, True)
            for enemy_hit in hits_player_bullet_enemy:
                puntuacion += enemy_hit.puntos

            hits_enemy_bullet_player = pygame.sprite.spritecollide(jugador, enemy_bullets, True)
            if hits_enemy_bullet_player:
                jugador.destruir()
                en_juego = False

            hits_enemy_player = pygame.sprite.spritecollide(jugador, enemy_group, False)
            if hits_enemy_player:
                jugador.destruir()
                en_juego = False

            if not enemy_group:
                en_juego = False

        ventana.blit(fondoimagen, (0, 0))

        all_sprites.draw(ventana)

        text_puntuacion = fuente_puntuacion.render(f"Puntos: {puntuacion}", True, VERDE_PUNTOS)
        ventana.blit(text_puntuacion, (10, 10))

        if pausado:
            s = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
            s.fill(GRIS_TRANSPARENTE)
            ventana.blit(s, (0, 0))

            dibujar_texto(ventana, "PAUSA", fuente_pausa_titulo, BLANCO, ANCHO // 2, ALTO // 4)

            mouse_pos = pygame.mouse.get_pos()
            dibujar_boton(ventana, boton_reanudar_rect, "Reanudar", fuente_pausa_boton, AZUL_CLARO, GRIS_CLARO,
                          mouse_pos)
            dibujar_boton(ventana, boton_menu_principal_rect, "Menú Principal", fuente_pausa_boton, AZUL_CLARO,
                          GRIS_CLARO, mouse_pos)

        pygame.display.update()

    if jugador.vida:
        mensaje_final = "¡Victoria!"
        color_mensaje = VERDE_PUNTOS
    else:
        mensaje_final = "Fin del Juego"
        color_mensaje = GRIS_OSCURO

    text_fin_juego_render = fuente_fin_juego.render(mensaje_final, True, color_mensaje)

    ventana.blit(text_fin_juego_render, (ANCHO // 2 - text_fin_juego_render.get_width() // 2,
                                         ALTO // 2 - text_fin_juego_render.get_height() // 2))
    pygame.display.update()
    pygame.time.wait(2000)

    return puntuacion, jugador.vida