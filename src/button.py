import pygame
pygame.init()

class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, img_file, text):
        '''
        Initialized with its name, rectangle, coordinates and text
        args(x:int, y:int, img_file:image, text:str) x: x Coordinate for the button, y: y coordinate for the button, img_file:an image to be the button, text:The text the button displays 
        '''
        
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(img_file).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y 
        
        self.text = text
    


    def update(self, new_text):
        '''
        Updates the old text over the button to the new text, which in this case would be the names of the trends the user will be guessing between 
        args:(new_text:str) The next text the button will display
        return:None
        '''
        self.text = new_text
        

