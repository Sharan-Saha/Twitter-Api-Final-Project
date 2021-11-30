import pathlib #Do we need this? Say's its unused
import sys
import json
from pathlib import Path
import pygame
import pygame_menu

from src import button
from src import label

class Controller: 
    def __init__(self, width = 1000, height = 800):
        pygame.init()
        
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        
        pygame.display.set_caption("Moore or Less")
        samoore = pygame.image.load('assets/samoore.jpg').convert_alpha()
        pygame.display.set_icon(samoore)
        
        self.background = pygame.Surface(self.screen.get_size()).convert()
        self.background.fill([250, 250, 250])  # set the background to white
    
        self.state = "MAIN_MENU"
        
        self.player_name = "Player"
        self.current_mode = "Test"
        
        pygame.font.init()
        self.font = pygame.font.SysFont('Comic Sans MS', 30)


        self.score = 0
        self.high_score = 0

        
        self.button1 = button.Button(50, 500, "assets/Button.png", "+1 Score") #NOTE: CHANGE OFF OF TEST
        self.button2 = button.Button(650, 500, "assets/Button.png", "END SCREEN")
        
        self.buttons = pygame.sprite.Group()
        self.buttons.add(self.button1)
        self.buttons.add(self.button2)
        
        
        
        self.label = label.Label(75,125, "assets/label.png", "This is a test")
        
        self.labels = pygame.sprite.Group()
        self.labels.add(self.label)
        

    def mainLoop(self):
        '''
        The loop which lets us go between the five states of the game. When the mode changes, the loop we are currently running also changes
        
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
        '''
        The main game loop. Deals with scoring, blitting objects to the screen, and events
        
        '''
        #resets scores and highscore
        self.score = 0
        self.high_score = 0 
        
        #updates highscore to match player data
        if self.player_name in self.leaderboard:
            self.high_score = self.leaderboard[self.player_name]
            
            
        while self.state == "GAME":
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if(event.key == pygame.K_q):
                        sys.exit()
                if pygame.mouse.get_pressed()[0]:
                    position = pygame.mouse.get_pos()
            
                    if self.button1.rect.collidepoint(position):
                            self.score +=1 

                            # self.button1.rect = self.button1.rect.inflate(-10,-10)
                            
                            #updates display before the short delay
                            pygame.display.flip()
                            pygame.time.wait(100)
                            # self.button1.rect.inflate_ip(-10,-10)

                        
                    elif self.button2.rect.collidepoint(position):
                            self.state = "END"
                            
                            #Only updates save & leaderboard if the score is the player's highscore
                            if self.score > self.leaderboard[self.player_name]:
                                self.leaderboard.update({self.player_name: self.score})
                            
                                path = Path('src/userinfo.json')
                                with open(path, 'w') as outfile:
                                    json.dump(self.leaderboard, outfile)

            #updates high score in real time 
            if self.score >= self.high_score:
                self.high_score = self.score
                            
            
            
            #Puts background, button text, and buttons(rectangles) on the screen
            self.screen.blit(self.background, (0, 0))
            
        
    
            self.buttons.draw(self.screen)
            
            self.labels.draw(self.screen)
            
            button1txt = self.font.render(self.button1.text, True, (250,50,50))
            # button1txt_rect = button1txt.get_rect()
            # button1txt_rect.center = (self.button1.width, button1txt_rect.height // 2)
            button2txt = self.font.render(self.button2.text, True, (250,50,50))
            
            
            self.screen.blit(button1txt, (self.button1.rect.x + 75,self.button1.rect.y + 25 ))
            self.screen.blit(button2txt, (self.button2.rect.x + 50,self.button2.rect.y + 25 ))

            #displays and updates specific users high score on screen
            high_score_board = self.font.render(f"High Score:{self.high_score}", True, (0,0,0))
            high_score_board_rect = high_score_board.get_rect()
            high_score_board_rect.center = (self.width // 2, self.height // 5)
            self.screen.blit(high_score_board, high_score_board_rect)

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
        self.main_menu.add.text_input('Name :', default=self.player_name, onchange=self.update_name)
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
         
        #Gets an updated version of player stats and leaderboard upon game start
        path = Path('src/userinfo.json')
        with open(path) as readfile:
            self.leaderboard = json.load(readfile)
            
        if self.player_name not in self.leaderboard: #If you aren't already in the leaderboard, your name is added
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
        Exits main menu and changes mode to leaderboard
        '''
        self.main_menu.disable()
        self.state = "LEADERBOARD"
    
    def leaderboardLoop(self):
        '''
        Sets up the leaderboard menu. Accesses leaderboard for most recent scores, sorts the scores, and displays them
        Args: None
        Returns: None
        '''
        
        self.leaderboard_menu = pygame_menu.Menu("Leaderboard", 1000, 800, theme=pygame_menu.themes.THEME_BLUE)
        path = Path('src/userinfo.json')
        
        with open(path) as readfile: #Updates the current leaderboard
             self.leaderboard = json.load(readfile)

        current_highscores = sorted(self.leaderboard.items(), key=lambda item: item[1], reverse = True )
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
        Exits leaderboard menu and changes mode to main menu
        
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
        
        



