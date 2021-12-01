import pygame
pygame.init()

class Label(pygame.sprite.Sprite):
    def __init__(self, x, y, img_file, text):
        '''
        Initialized with its name, rectangle, coordinates and text
        
        '''
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(img_file).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y 
        self.text = text
    
    def update(self, new_text):
        '''
        updates old text for label for new text. Old text should just be the question: "{base_trend} or {comparison_trend} ?" and after the 
        button is clicked it should update to message saying if choice was correct
        parameters: self, new_text
        returns: none
        '''
        self.text = new_text
