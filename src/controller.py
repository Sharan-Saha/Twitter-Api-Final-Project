import sys
import json
from pathlib import Path
import pygame
import pygame_menu

from src import button

class Controller: 
    def __init__(self, width = 1000, height = 800):
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
        self.font = pygame.font.SysFont('Comic Sans MS', 30)


        self.score = 0


        self.buttons = pygame.sprite.Group()
        self.button1 = button.Button(50, 500, "assets/Button.png", "Test")
        self.button2 = button.Button(650, 500, "assets/Button.png", "Test2")
        
        self.buttons.add(self.button1)
        self.buttons.add(self.button2)

    def mainLoop(self):
        '''
        The five states of the game. When the mode changes, the loop we run also changes
        
        '''
        while True:
            if self.state == "MAIN_MENU":
                self.menuLoop()
                
            elif self.state =="SETTINGS":
                self.settingsLoop()
                
            elif self.state == "GAME":
                self.gameLoop()
                
            elif self.state == "LEADERBOARD":
                self.leaderboardLoop()
                
            elif self.state == "END":
                self.endLoop()

    def gameLoop(self):
        while self.state == "GAME":
            for event in pygame.event.get():
            
                if event.type == pygame.KEYDOWN:
                    if(event.key == pygame.K_q):
                        sys.exit()
                if pygame.mouse.get_pressed()[0]:
                    position = pygame.mouse.get_pos()
            
                    if self.button1.rect.collidepoint(position):
                            self.score +=1 
                            print(f"Score:{self.score}")
                            # self.button1.rect = self.button1.rect.inflate(-10,-10)
                            pygame.display.flip()
                            pygame.time.wait(100)
                            # self.button1.rect.inflate_ip(-10,-10)

                        
                    elif self.button2.rect.collidepoint(position):
                            self.state = "END"
                            self.leaderboard.update({self.player_name: self.score})
                            
                            path = Path('src/userinfo.json')
                            with open(path, 'w') as outfile:
                                json.dump(self.leaderboard, outfile)
                            self.score = 0
            
            
            #Puts background, button text, and buttons(rectangles) on the screen
            self.screen.blit(self.background, (0, 0))
            
        
    
            self.buttons.draw(self.screen)
            button1txt = self.font.render("button1", True, (250,50,50))
            # button1txt_rect = button1txt.get_rect()
            # button1txt_rect.center = (self.button1.width, button1txt_rect.height // 2)

            button2txt = self.font.render("End Screen", True, (250,50,50))
            self.screen.blit(button1txt, self.button1.rect.midleft)
            self.screen.blit(button2txt, self.button2.rect.midleft)

            #displays and updates score on screen
            score_board = self.font.render(f"Score:{self.score}", True, (0,0,0))
            score_board_rect = score_board.get_rect()
            score_board_rect.center = (self.width // 2, self.height // 4)
            self.screen.blit(score_board, score_board_rect)
            
            pygame.display.flip()
        
    def settingsLoop(self):
        pass
    
    
    def menuLoop(self):
       '''
       Sets up our menu.
       '''
       self.main_menu = pygame_menu.Menu('Moore or Less!?', 1000, 800, theme=pygame_menu.themes.THEME_BLUE)
       self.main_menu.add.text_input('Name :', default='Player', onchange=self.update_name)
       self.main_menu.add.selector('Mode :', [('Normal', 1), ('Timed', 2), ('Endless', 3)], onchange=self.set_mode)
       self.main_menu.add.button('Play', self.start_the_game)
       self.main_menu.add.button('Settings', self.view_settings)
       self.main_menu.add.button('Leaderboard', self.view_leaderboard)
       self.main_menu.add.button('Quit', pygame_menu.events.EXIT)
       
       
       self.main_menu.mainloop(self.screen)
       pygame.display.flip()
        
    def start_the_game(self):
         '''
         Exits menu and changes mode
         
         '''
        
         self.main_menu.disable()
         
         path = Path('src/userinfo.json')
         with open(path) as readfile:
             self.leaderboard = json.load(readfile)
         self.leaderboard.update({self.player_name: self.score})
         with open(path, 'w') as outfile:
            json.dump(self.leaderboard, outfile)
         self.state = "GAME"
         
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
        
        
    def view_settings(self):
        '''
        Goes to settings
        '''
        pass
    
    def view_leaderboard(self):
        '''
        Exits menu and changes mode
        '''
        self.main_menu.disable()
        self.state = "LEADERBOARD"
    
    def leaderboardLoop(self):
        """
        Sets up the leaderboard menu. Accesses leaderboard for most recent scores, sorts the scores, and displays them
        Args: None
        Returns: None
        """
        
        self.leaderboard_menu = pygame_menu.Menu("Leaderboard", 1000, 800, theme=pygame_menu.themes.THEME_BLUE)
        path = Path('src/userinfo.json')
        
        with open(path) as readfile: #Updates the current leaderboard
             self.leaderboard = json.load(readfile)

        current_highscores = sorted(self.leaderboard.items(), key=lambda item: item[1], reverse = True )
        print(current_highscores)
        for i in range(0,10):
            if i >= len(current_highscores): #Adds filler scores if there is less than 10 people on the leaderboard
                self.leaderboard_menu.add.label(f"{i+1}. Player || SCORE:N/A") 
            else:
                self.leaderboard_menu.add.label(f"{i+1}. {current_highscores[i][0]} || SCORE:{current_highscores[i][1]}") #Adds player scores
        self.leaderboard_menu.add.button("Main Menu", self.go_to_menu_leaderboard)
        self.leaderboard_menu.mainloop(self.screen)
        pygame.display.flip()
      
    def go_to_menu_leaderboard(self):
        '''
        Exits menu and changes mode
        
        '''
        self.leaderboard_menu.disable()
        self.state = "MAIN_MENU"
      
        
      
        
    def endLoop(self):
        '''
        Sets up the game over menu.
        '''
        self.end = pygame_menu.Menu('Game Over!', 1000, 800, theme=pygame_menu.themes.THEME_BLUE)
        self.end.add.label(f"Score:{self.score}")
        self.end.add.button('Play again', self.restart_the_game)
        self.end.add.button('Main Menu', self.go_to_menu_end)
        self.end.add.button('Leaderboard', self.view_leaderboard_end)
        self.end.add.button('Quit', pygame_menu.events.EXIT)
        
        self.end.mainloop(self.screen)
        pygame.display.flip()
        
    def restart_the_game(self):
        '''
        Exits menu and changes mode
        '''
        print(f"{self.player_name} play {self.current_mode}")
        self.end.disable()
        self.state = "GAME"
    
    def go_to_menu_end(self):
        '''
        Exits menu and changes mode
        '''
        self.end.disable()
        self.state = "MAIN_MENU"
        
    def view_leaderboard_end(self):
        '''
        Exits menu and changes mode
        '''
        self.end.disable()
        self.state = "LEADERBOARD"    
        
        



