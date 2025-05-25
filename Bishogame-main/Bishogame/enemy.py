# enemy.py - Contiene la clase noCreyente (el enemigo)

import pygame
import sys
from random import randint
from config import VELOCIDAD_ENEMIGO_MOV, DESPLAZAMIENTO_VERTICAL_ENEMIGO, IMAGEN_DISPARO_ENEMIGO, \
    FRECUENCIA_DISPARO_ENEMIGO
from bullet import Balon


class noCreyente(pygame.sprite.Sprite):
    def __init__(self, posx, posy, distancia, imguno, imgdos, puntos,
                 escala=1.0):  # ¡CAMBIO! Añadido argumento 'escala'
        super().__init__()
        try:
            # Cargar imágenes y escalarlas
            img_original1 = pygame.image.load(imguno).convert_alpha()
            img_original2 = pygame.image.load(imgdos).convert_alpha()

            # Escalar imágenes
            self.images = [
                pygame.transform.scale_by(img_original1, escala),  # ¡CAMBIO! Escalar imágenes
                pygame.transform.scale_by(img_original2, escala)  # ¡CAMBIO! Escalar imágenes
            ]
        except pygame.error as e:
            print(f"Error al cargar imágenes de enemigo ({imguno}, {imgdos}): {e}")
            pygame.quit()
            sys.exit()

        self.posImg = 0
        self.image = self.images[self.posImg]
        self.rect = self.image.get_rect()
        self.rect.top = posy
        self.rect.left = posx

        self.velocidad = VELOCIDAD_ENEMIGO_MOV
        self.rango_disparo_chance = FRECUENCIA_DISPARO_ENEMIGO  # ¡CAMBIADO! Usamos la constante
        self.ultimo_cambio_img = 0
        self.tiempo_cambio_img = 200

        self.derecha = True
        self.contador_mov_lateral = 0
        self.max_descenso_actual = self.rect.top + DESPLAZAMIENTO_VERTICAL_ENEMIGO

        self.limiteder = posx + distancia
        self.limiteizq = posx - distancia
        self.puntos = puntos

    def update(self, current_time):
        if self.contador_mov_lateral < 3:
            self.__movimiento_lateral()
        else:
            self.__descenso()

        if current_time - self.ultimo_cambio_img > self.tiempo_cambio_img:
            self.posImg = (self.posImg + 1) % len(self.images)
            self.image = self.images[int(self.posImg)]
            self.ultimo_cambio_img = current_time

    def __movimiento_lateral(self):
        if self.derecha:
            self.rect.x += self.velocidad
            if self.rect.right > self.limiteder:
                self.derecha = False
                self.contador_mov_lateral += 1
        else:
            self.rect.x -= self.velocidad
            if self.rect.left < self.limiteizq:
                self.derecha = True
                self.contador_mov_lateral += 1

    def __descenso(self):
        if self.rect.y < self.max_descenso_actual:
            self.rect.y += 1
        else:
            self.contador_mov_lateral = 0
            self.max_descenso_actual = self.rect.y + DESPLAZAMIENTO_VERTICAL_ENEMIGO

    def atacar(self):
        # ¡CAMBIO! La probabilidad de disparo ahora se basa en FRECUENCIA_DISPARO_ENEMIGO
        # un número más alto significa que disparen menos.
        if randint(1, 100) > self.rango_disparo_chance:  # Por ejemplo, si es 98, solo dispara si randint es 99 o 100
            return Balon(self.rect.centerx, self.rect.bottom, IMAGEN_DISPARO_ENEMIGO, False)
        return None