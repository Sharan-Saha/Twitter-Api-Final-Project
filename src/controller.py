import sys
import pygame

from src import button

class Controller: 
    def __init__(self, width=800, height = 800):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.background = pygame.Surface(self.screen.get_size()).convert()
        self.background.fill([250, 250, 250])  # set the background to white
    
        self.state = "ON"

        self.buttons = pygame.sprite.Group()
        self.buttons.add(button.Button("button1", 150, 500, "assets/Button.png"))

    def mainLoop (self):
        if self.state == "ON":
            self.gameLoop()

    def gameLoop(self):
        while self.state == "ON":
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if(event.key == pygame.K_LEFT):
                        sys.exit()
            self.screen.blit(self.background, (0,0))
            self.buttons.draw(self.screen)
            pygame.display.flip()
        

