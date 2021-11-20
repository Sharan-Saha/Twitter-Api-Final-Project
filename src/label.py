from typing import Text
import pygame
pygame.init()

class Label(pygame.sprite.Sprite):
    def __init__(self, name, x, y, img_file):
        self.name = name
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y 
        self.text = Text
    
    def update(self, new_text):
        """
            updates old text for label for new text. Old text should just be the question: "{base_trend} or {comparison_trend} ?" and after the 
            button is clicked it should update to message saying if choice was correct
            parameters: self, new_text
            returns: none
        """
        self.text = new_text