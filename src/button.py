import pygame
pygame.init()

class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, img_file, text):
        '''
        Initialized with its name, rectangle, coordinates and text
        args(int, int, image, str) needs coordinates for the button, an image to be the button and the text the button displays 
        '''
        
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(img_file).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y 
        
        self.text = text
    


    def update(self, new_text):
        '''
        updates the old text over the button to the new text, which in this case would be the names of the trends the user will be guessing between 
        parameters: self, self.text new_text
        args:None
        return:None
        '''
        self.text = new_text
        

