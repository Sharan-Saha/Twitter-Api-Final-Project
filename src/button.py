import pygame
pygame.init()

class Button(pygame.sprite.Sprite):
    def __init__(self, name, x, y, img_file, text):

        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(img_file).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y 
        self.text = text
    
    def hover(self, mouse_x, mouse_y):
        #not sure if this should be in this class or in the controller class
        return True

    def update(self, new_text):
        """
            updates the old text over the button to the new text, which in this case would be the names of the trends the user will be guessing between 
            parameters: self, self.text new_text
        """
        self.text = new_text
