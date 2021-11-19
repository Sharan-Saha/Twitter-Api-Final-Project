from src import OddEven
from src import Button
import pygame
import pygame_menu
pygame.init()


class Controller:
    
    
    def __init__(self):
        '''
        Sets up everythin controller needs
        '''
        #Window stuff
        self.window_width = 1000
        self.window_height = 800
        #game mode
        self.mode = "MAIN_MENU"
        #Makes our generator which generates 1 or 2
        self.generator= OddEven.OddEven()
        #Necessary game stats
        self.score = 0
        self.name = "Player"
        self.lives = 3
        self.running = True
        #So our font works
        pygame.font.init()
        self.font=pygame.font.Font('freesansbold.ttf',24)
        
        #Sets up screen, background and our buttons
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        self.background = pygame.Surface(( self.window_width, self.window_height))
        self.background.fill((150,150,150))
        self.odd_button = Button.Button(self.window_width/5,self.window_height/3,150,50,"Odd")
        self.even_button = Button.Button(self.window_width*.7, self.window_height/3,150,50,"Even")
        
       
    def mainLoop(self):
        '''
        The three states of the game. When the mode changes, the loop we run also changes
        
        '''
        while self.running:
            if self.mode == "MAIN_MENU":
                self.menuLoop()
                
            elif self.mode == "GAME":
                self.gameLoop()
                
            elif self.mode == "END":
                self.endLoop()
                
    def menuLoop(self):
        '''
        Sets up our menu. See me (clay) if u dont understand this cuz its weird
        '''
        self.menu = pygame_menu.Menu('Moore or Less!?', 800, 600, theme=pygame_menu.themes.THEME_BLUE)
        self.menu.add.text_input('Name :', default='Player', onchange=self.update_name)
        self.menu.add.selector('Mode :', [('Normal', 1), ('Timed', 2)], onchange=self.set_mode)
        self.menu.add.button('Play', self.start_the_game)
        self.menu.add.button('Quit', pygame_menu.events.EXIT)
        self.player_name = "Player"
        self.current_mode = "Normal"
        
        self.menu.mainloop(self.screen)
        pygame.display.flip()
        
    def start_the_game(self):
        '''
        Exits menu and changes mode
        
        '''
        print(f"{self.player_name} play {self.current_mode}")
        self.menu.disable()
        self.mode = "GAME"
        
    def restart_the_game(self):
        '''
        Exits menu and changes mode
        
        '''
        print(f"{self.player_name} play {self.current_mode}")
        self.end.disable()
        self.mode = "GAME"
    
    def go_to_menu(self):
        '''
        Exits menu and changes mode
        
        '''
        self.end.disable()
        self.mode = "MAIN_MENU"
        
    def set_mode(self, mode, option):
        '''
        Doesn't do anything rn, but in the future would swithc it to a timed mode
        
        '''
        self.current_mode = mode[0][0]
        self.options = option
        print("Toggled.")
        
    
    def update_name(self, name):
        '''
        When player changes their name, the controller keeps track of that
        '''
        self.player_name = name
            
    
    
    def gameLoop(self):
        
        '''
        see comments
        
        '''
        
        
        #resets statistics
        
        self.number = self.generator.odd_or_even()
        self.score = 0
        self.lives = 3
        
        while self.mode=="GAME":
            
            #renders the text we display
            display_number = self.font.render(str(self.number), True, (250,50,50))
            lives = self.font.render(f"Lives:{self.lives}", True, (250,50,50))
            self.eventLoop()
            
            #Puts background, numbers, button text, and buttons(rectangles) on the screen
            self.screen.blit(self.background, (0, 0))
            
            self.screen.blit(display_number, (self.window_width/2, self.window_height/7))
            
            self.screen.blit(self.odd_button.screen_text, self.odd_button.rect.midtop)
            self.screen.blit(self.even_button.screen_text, self.even_button.rect.center)
            
            self.screen.blit(lives, (self.window_width/2, 300))
            
            pygame.draw.rect(self.background, (0,0,0), self.odd_button.rect_stats)
            pygame.draw.rect(self.background, (0,0,0), self.even_button.rect_stats)
            
            
            #Screen shows new changes
            pygame.display.flip()    
            
            
    def eventLoop(self):    
        '''
        The different events that can happen. Either quitting, a button being pressed, or the game ending
        '''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
                
                #If the mouse is clicked while over the button, the following code is executed
            if pygame.mouse.get_pressed()[0]:
                position = pygame.mouse.get_pos()
                print(pygame.mouse.get_pos())
            
                if self.odd_button.rect.collidepoint(position):
                    if self.number == 1:
                        print("YES!")
                        self.score +=1
                    else:
                        print("no")
                        self.lives-=1
                    self.number = self.generator.odd_or_even()
                elif self.even_button.rect.collidepoint(position):
                    if self.number == 2:
                        print("YES!")
                    else:
                        print("no")
                        self.lives-=1
                    self.number = self.generator.odd_or_even()
                    
                    #If u run out of lives the game goes to game over screen
        if self.lives <= 0:
            self.mode = "END"
            
        

    def endLoop(self):
        '''
        Sets up the game over menu. See me (clay) if u dont understand this cuz its weird
        '''
        self.end = pygame_menu.Menu('Game Over!', 800, 600, theme=pygame_menu.themes.THEME_BLUE)
        self.end.add.label(f"Score:{self.score}")
        self.end.add.button('Play again', self.restart_the_game)
        self.end.add.button('Main Menu', self.go_to_menu)
        self.end.add.button('Quit', pygame_menu.events.EXIT)
        
        self.end.mainloop(self.screen)
        pygame.display.flip()
        
    