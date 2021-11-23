import sys
import pygame
import pygame_menu

from src import button

class Controller: 
    def __init__(self, width = 800, height = 800):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.background = pygame.Surface(self.screen.get_size()).convert()
        self.background.fill([250, 250, 250])  # set the background to white
    
        self.state = "MAIN_MENU"
        
        self.player_name = "Player"
        self.current_mode = "Test"
        
        pygame.font.init()
        myfont = pygame.font.SysFont('Comic Sans MS', 30)

        self.textsurface = myfont.render('Some Text', False, (0, 0, 0))


        #self.buttons = pygame.sprite.Group()
        #self.buttons.add(button.Button("button1", 150, 500, "assets/Button.png"))

    def mainLoop(self):
        '''
        The four states of the game. When the mode changes, the loop we run also changes
        
        '''
        while True:
            if self.state == "MAIN_MENU":
                self.menuLoop()
                
            elif self.state =="SETTINGS":
                self.settingsLoop()
                
            elif self.state == "GAME":
                self.gameLoop()
                
            elif self.state == "END":
                self.endLoop()

    def gameLoop(self):
        while self.state == "GAME":
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if(event.key == pygame.K_LEFT):
                        sys.exit()
            self.screen.blit(self.textsurface,(0,0))
            self.screen.blit(self.background, (0,0))
            
            self.buttons.draw(self.screen)
            pygame.display.flip()
        
    def settingsLoop(self):
        pass
    
    
    def menuLoop(self):
       '''
       Sets up our menu. See me (clay) if u dont understand this cuz its weird
       '''
       self.menu = pygame_menu.Menu('Moore or Less!?', 800, 600, theme=pygame_menu.themes.THEME_BLUE)
       self.menu.add.text_input('Name :', default='Player', onchange=self.update_name)
       self.menu.add.selector('Mode :', [('Normal', 1), ('Timed', 2)], onchange=self.set_mode)
       self.menu.add.button('Play', self.start_the_game)
       self.menu.add.button('Quit', pygame_menu.events.EXIT)
       
       
       self.menu.mainloop(self.screen)
       pygame.display.flip()
        
    def start_the_game(self):
         '''
         Exits menu and changes mode
         
         '''
         print(f"{self.player_name} play {self.current_mode}")
         self.menu.disable()
         self.mode = "GAME"
         
    def update_name(self, name):
        '''
        When player changes their name, the controller keeps track of that
        '''
        self.player_name = name
    
    def set_mode(self, mode, option):
        '''
        Doesn't do anything rn, but in the future would swithc it to a timed mode
        
        '''
        self.current_mode = mode[0][0]
        print("Toggled.", option)    
        
        
        
        
        
        



