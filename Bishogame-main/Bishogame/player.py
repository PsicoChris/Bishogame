# player.py - Contiene la clase BishoSiu (el jugador)

import pygame
import sys
from config import ANCHO, ALTO, VELOCIDAD_JUGADOR, IMAGEN_BISHO, IMAGEN_BALON_JUGADOR
from bullet import Balon


class BishoSiu(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        try:
            self.image = pygame.image.load(IMAGEN_BISHO).convert_alpha()
        except pygame.error as e:
            print(f"Error al cargar la imagen del Bisho ({IMAGEN_BISHO}): {e}")
            pygame.quit()
            sys.exit()
        self.rect = self.image.get_rect()
        self.rect.centerx = ANCHO // 2
        self.rect.centery = ALTO - 30
        self.velocidad = VELOCIDAD_JUGADOR
        self.vida = True

        # Para movimiento continuo
        self.moviendo_izquierda = False
        self.moviendo_derecha = False

    def update(self, current_time):  # Asegúrate de que acepta current_time
        if self.vida:
            # Lógica de movimiento continuo
            if self.moviendo_izquierda:
                self.rect.x -= self.velocidad
            if self.moviendo_derecha:
                self.rect.x += self.velocidad

            # Asegurarse de que el jugador no salga de los límites de la pantalla
            if self.rect.left < 0:
                self.rect.left = 0
            elif self.rect.right > ANCHO:
                self.rect.right = ANCHO

    def movDer(self):
        # Este método ahora solo establece la bandera de movimiento
        self.moviendo_derecha = True

    def movIzq(self):
        # Este método ahora solo establece la bandera de movimiento
        self.moviendo_izquierda = True

    # ¡NUEVO MÉTODO! Para detener el movimiento al soltar la tecla
    def detener_movimiento(self, direccion):
        if direccion == "izquierda":
            self.moviendo_izquierda = False
        elif direccion == "derecha":
            self.moviendo_derecha = False

    def cabecear(self):
        if self.vida:
            return Balon(self.rect.centerx, self.rect.top, IMAGEN_BALON_JUGADOR, True)
        return None

    def destruir(self):
        self.vida = False
        self.velocidad = 0