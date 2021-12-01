import pygame
pygame.init()

class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, img_file, text, width=100, height=50):
        '''
        Initialized with its name, rectangle, coordinates and text
        
        '''
        
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(img_file).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y 
        self.width = width
        self.height = height
        
        self.text = text
    
# =============================================================================
#     def hover(self, mouse_x, mouse_y):
#         #not sure if this should be in this class or in the controller class
#         '''
#         Checks to see if the x and y coordinates of the mouse are within the range of the button size and if it is it return's true
#         '''
#         if mouse_x <= self.x + self.width and mouse_y <= self.y + self.height:
#             return True
#         else:
#             return False
# =============================================================================

    def update(self, new_text):
        '''
        updates the old text over the button to the new text, which in this case would be the names of the trends the user will be guessing between 
        parameters: self, self.text new_text
        '''
        self.text = new_text
        
    def ifClicked(self):
        '''
        If button is clicked, returns true
        '''

        return True
