# bullet.py - Contiene la clase Balon (los proyectiles)

import pygame
import sys
from config import VELOCIDAD_BALON_JUGADOR, VELOCIDAD_BALON_ENEMIGO, ALTO

class Balon(pygame.sprite.Sprite):
    def __init__(self, posx, posy, ruta_imagen, es_jugador):
        super().__init__()
        try:
            self.image = pygame.image.load(ruta_imagen).convert_alpha()
        except pygame.error as e:
            print(f"Error al cargar la imagen del balón ({ruta_imagen}): {e}")
            pygame.quit()
            sys.exit()
        self.rect = self.image.get_rect()
        self.rect.centerx = posx
        self.rect.centery = posy

        self.velocidad = VELOCIDAD_BALON_JUGADOR if es_jugador else VELOCIDAD_BALON_ENEMIGO
        self.es_disparo_jugador = es_jugador

    # ¡CAMBIO AQUÍ! Añade 'current_time' como argumento
    def update(self, current_time):
        """
        Actualiza el estado del balón.
        'current_time' se pasa desde el grupo de sprites, aunque no se use directamente aquí.
        """
        if self.es_disparo_jugador:
            self.rect.y -= self.velocidad
        else:
            self.rect.y += self.velocidad

        # Eliminar balones que salen de la pantalla
        if self.rect.bottom < 0 or self.rect.top > ALTO:
            self.kill() # Elimina el sprite de todos los grupos a los que pertenece