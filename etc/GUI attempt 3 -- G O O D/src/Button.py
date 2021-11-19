import pygame
pygame.init 

class Button:
    
    def __init__(self, x, y, w, h, text):
        '''
        sets the button (which is effectively a rectangle rn) location, width, height and its text
        
        
        '''
        self.upper_left_coords=(x,y)
        self.width = w
        self.height = h
        self.rect = pygame.Rect(x,y, w, h)
        self.rect_stats = [x,y, w, h]
        self.clicked = False
        self.text = text
        pygame.font.init()
        font=pygame.font.Font('freesansbold.ttf',24)
        self.screen_text= font.render(text, True, (250, 250 ,250))
    
        
        
    def ifClicked(self):
        '''
        This is called if clicked, returns true
        '''
        return True