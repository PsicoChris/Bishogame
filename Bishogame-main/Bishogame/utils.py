# utils.py - Funciones auxiliares generales

import pygame
from config import NEGRO # Importamos el color NEGRO de config

def dibujar_texto(superficie, texto, fuente, color, x, y):
    """
    Dibuja texto centrado en la superficie.
    """
    texto_superficie = fuente.render(texto, True, color)
    texto_rect = texto_superficie.get_rect()
    texto_rect.center = (x, y)
    superficie.blit(texto_superficie, texto_rect)

def dibujar_boton(superficie, rect, texto, fuente, color_normal, color_hover, mouse_pos):
    """
    Dibuja un botón con texto y efecto hover.
    Retorna True si el ratón está sobre el botón, False en caso contrario.
    """
    color_actual = color_normal
    if rect.collidepoint(mouse_pos):
        color_actual = color_hover
    pygame.draw.rect(superficie, color_actual, rect, border_radius=10) # Borde redondeado
    dibujar_texto(superficie, texto, fuente, NEGRO, rect.centerx, rect.centery)
    return rect.collidepoint(mouse_pos) # Retorna si el ratón está sobre el botón