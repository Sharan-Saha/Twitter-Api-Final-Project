import sys
import json
import random
from pathlib import Path
from src import apiCall
import pygame
import pygame_menu

from src import button
from src import label


class Controller: 
    def __init__(self, width = 1000, height = 800):
        '''
        Sets up the things we need for the game to run. The screen, background, window, font, variables the game needs to run, buttons and labels
        args(int, int) Width and height can be changed, but are default 1000 and 800
        '''
        pygame.init()
        
        #Screen setup
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        
        #Game window name and icon
        pygame.display.set_caption("Moore or Less")
        samoore = pygame.image.load('assets/samoore.jpg').convert_alpha()
        pygame.display.set_icon(samoore)
        
        #Background
        self.light_background = pygame.image.load('assets/Light_Background.png').convert()
        self.dark_background = pygame.image.load('assets/Dark_Background.png').convert()
        self.background = pygame.transform.scale(self.light_background, (1000, 800))
        self.current_theme = "Light"
    
        
        #Font setup
        pygame.font.init()
        self.default_font = pygame.font.SysFont('Arial', 40, bold=True)
        self.question_font = pygame.font.SysFont('Arial', 28, bold=True)
        self.score_font = pygame.font.SysFont('Arial', 30, bold=True)

        #Game Needs these to run
        self.score = 0
        self.high_score = 0
        self.same_number = False
        
        self.state = "MAIN_MENU"
        
        #Default names for game variables
        self.player_name = "Player"
        self.base_name = "base"
        self.comparison_name = "comparison" 
        self.base_count = 0

        #Defines an Api call object to get our new trends 
        self.apiCall = apiCall.ApiCall()
        self.apiCall.getTrends()
        
        
        #adds our buttons
        self.moore_button = button.Button(50, 500, "assets/Button.png",  "Moore") 
        self.less_button = button.Button(650, 500, "assets/Button.png", "Less")
        
        self.buttons = pygame.sprite.Group()
        self.buttons.add(self.moore_button)
        self.buttons.add(self.less_button)
          
        #Sets up leaderboard path and creates a new userinfo file if one does not exist
        self.leaderboard_path = Path('src/userinfo.json')
        if not self.leaderboard_path.is_file(): 
            with open(self.leaderboard_path, 'w') as createfile:
                json.dump({}, createfile)

        
        #adds our labels
        self.labels = pygame.sprite.Group()
      
        
        self.scores_label = label.Label(350,25, "assets/smalllabel.png", "I show scores")
        self.question_label_b = label.Label(75,125, "assets/label.png", f"{self.base_name} has {self.base_count} tweets.")
        self.question_label_c = label.Label(75,125, "assets/label.png", f"Does {self.comparison_name} have moore or less tweets?")
        self.labels = pygame.sprite.Group()
        self.labels.add(self.scores_label)
        self.labels.add(self.question_label_b)
        self.labels.add(self.question_label_c)


    def mainLoop(self):
        '''
        The loop which lets us go between the five states of the game. When the mode changes, the loop we are currently running also changes
        args:None
        return:None
        '''
        while True:
            if self.state == "MAIN_MENU":
                self.menuLoop()
                
            elif self.state == "GAME":
                self.gameLoop()
                
            elif self.state == "LEADERBOARD":
                self.leaderboardLoop()
                
            elif self.state == "END":
                self.endLoop()

    def gameLoop(self):
        '''
        The main game loop. Deals with scoring, blitting objects to the screen, and events
        Has onetime setup which sets up the comparisons and text
        args:None
        return:None
        '''
        self.apiCall.getTrends() #Refreshes trends if more than 15 minutes have passed
        
        
        with open("src/trends.json") as trends: #reads the trends, makes a deck out with them, and removes the timestamp.
            self.deck = json.load(trends)
            self.deck.pop(0)
            self.deck.pop()
        
        ### This can all be a function

        #Randomly selects 2 trends
        self.base_number = random.randrange(0, len(self.deck))
        self.comparison_number = random.randrange(0, len(self.deck))


        if self.base_number == self.comparison_number: #If the trends are the same thing, we change that
            self.same_number = True
        
            while self.same_number:
                self.comparison_number = random.randrange(1, len(self.deck))
                if self.comparison_number != self.base_number:
                    self.same_number = False
        
        #Gets the tweet count for each topic
        self.base_count = self.deck[self.base_number][1]
        self.comparison_count = self.deck[self.comparison_number][1]


        #gets the name for each topic
        self.base_name = self.deck[self.base_number][0]
        self.comparison_name = self.deck[self.comparison_number][0]

        #Updates the label to include new information
        self.question_label_b.update(f"{self.base_name} has {self.base_count} tweets.")
        self.question_label_c.update(f"Does {self.comparison_name} have moore or less tweets?")
        
        #updates highscore to match player data
        if self.player_name in self.leaderboard:
            self.high_score = self.leaderboard[self.player_name]
            
        ###Until here
            
        while self.state == "GAME":
            
            self.screen.blit(self.background, (0,0))
            for event in pygame.event.get():
                #Can quit by hitting the x or pushing q
                if event.type==pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if(event.key == pygame.K_q):
                        sys.exit()
                        
                #clicking gets mouse pos and checks if buttons were clicked
                if event.type == pygame.MOUSEBUTTONUP:
                    position = pygame.mouse.get_pos()
            
                    if self.moore_button.rect.collidepoint(position):#If their guess is more
                            if self.base_count < self.comparison_count:#If the guess is correct... score!
                    
                                ###this can be a function
                                self.score +=1
                                
                                self.base_number = self.comparison_number  #Previous comparison trend becomes the new base trend
                                self.comparison_number = random.randrange(0, len(self.deck)) #Choses a new comparison trend

                                if self.base_number == self.comparison_number: #If the trends are the same thing, we change that
                                    self.same_number = True
        
                                    while self.same_number:
                                        self.comparison_number = random.randrange(1, len(self.deck))
                                        if self.comparison_number != self.base_number:
                                            self.same_number = False


                                #name updating
                                self.base_name = self.deck[self.base_number][0]
                                self.comparison_name = self.deck[self.comparison_number][0]

                                self.base_count = self.deck[self.base_number][1]
                                self.comparison_count = self.deck[self.comparison_number][1]
                                self.question_label_b.update(f"{self.base_name} has {self.base_count} tweets.")
                                self.question_label_c.update(f"Does {self.comparison_name} have moore or less tweets?")

                            else:
                                self.state = "END" #If guess is wrong, we end the game
                                if self.score > self.leaderboard[self.player_name]: #Only updates save & leaderboard if the score is the player's highscore
                                    self.leaderboard.update({self.player_name: self.score})

                                    with open(self.leaderboard_path, 'w') as outfile:
                                        json.dump(self.leaderboard, outfile)
                                        #func(bt,ct)
                                        # func(ct,bt)
                                        
                    elif self.less_button.rect.collidepoint(position):
                            if self.base_count > self.comparison_count:  #If their guess is less, correct!    
                    
                                self.score +=1
                                self.base_number = self.comparison_number #Previous comparison trend becomes the new base trend
                                self.comparison_number = random.randrange(0, len(self.deck)) #Choses a new comparison trend

                                if self.base_number == self.comparison_number: #If the trends are the same thing, we change that
                                    self.same_number = True
        
                                    while self.same_number:
                                        self.comparison_number = random.randrange(1, len(self.deck))
                                        if self.comparison_number != self.base_number:
                                            self.same_number = False

        
                                #Updating the names
                                self.base_name = self.deck[self.base_number][0]
                                self.comparison_name = self.deck[self.comparison_number][0]

                                self.base_count = self.deck[self.base_number][1]
                                self.comparison_count = self.deck[self.comparison_number][1]
                                self.question_label_b.update(f"{self.base_name} has {self.base_count} tweets.")
                                self.question_label_c.update(f"Does {self.comparison_name} have moore or less tweets?")
                                
                            else:
                                self.state = "END" #Guess was incorrect, game ends
                                if self.score > self.leaderboard[self.player_name]: #Only updates save & leaderboard if the score is the player's highscore
                                    self.leaderboard.update({self.player_name: self.score})

                                    with open(self.leaderboard_path, 'w') as outfile:
                                        json.dump(self.leaderboard, outfile)
                           
                            

            #updates high score in real time 
            if self.score >= self.high_score:
                self.high_score = self.score
                            
            
            
            #Puts background, button text, and buttons(rectangles) on the screen
            self.screen.blit(self.background, (0, 0))
            
            
            self.buttons.draw(self.screen)
            self.labels.draw(self.screen)
        
            #Renders the text
            moore_button_txt = self.default_font.render(self.moore_button.text, True, (0,0,0))
            less_button_txt = self.default_font.render(self.less_button.text, True, (0,0,0))
            question_label_b_txt = self.question_font.render(self.question_label_b.text, True, (0,0,0))
            question_label_c_txt = self.question_font.render(self.question_label_c.text, True, (0,0,0))

            #assigns center and blits text on screen
            
            question_label_b_rect = question_label_b_txt.get_rect()
            question_label_b_rect.center = (self.width // 2, ((self.question_label_b.rect.y + 35)))
            self.screen.blit(question_label_b_txt, question_label_b_rect)
            question_label_c_rect = question_label_c_txt.get_rect()
            question_label_c_rect.center = (self.width // 2, (self.question_label_b.rect.y) + 70)
            self.screen.blit(question_label_c_txt, question_label_c_rect)
            self.screen.blit(moore_button_txt, (self.moore_button.rect.x + 80, self.moore_button.rect.y + 25 ))
            ### Scooch the Less button text to the center of it's button
            self.screen.blit(less_button_txt, (self.less_button.rect.x + 80, self.less_button.rect.y + 25 ))

            #displays and updates specific users high score on screen
            high_score_board = self.score_font.render(f"High Score:{self.high_score}", True, (0,0,0))
            high_score_board_rect = high_score_board.get_rect()
            high_score_board_rect.center = (self.width // 2, ((self.height // 13)))
            self.screen.blit(high_score_board, high_score_board_rect)

            #displays and updates score on screen
            score_board = self.score_font.render(f"Score:{self.score}", True, (0,0,0))
            score_board_rect = score_board.get_rect()
            score_board_rect.center = (self.width // 2, ((self.height // 8)))
            self.screen.blit(score_board, score_board_rect)
            
            
            pygame.display.flip()
        
    
    def menuLoop(self):
        '''
        Sets up our main menu.
        args:None
        return:None
        '''
        if self.current_theme == "Light":#If the theme is light, lightmode is used. Otherwise the dark theme is used.
            self.main_menu = pygame_menu.Menu('Moore or Less!?', 1000, 800, theme=pygame_menu.themes.THEME_BLUE)
        else:
            self.main_menu = pygame_menu.Menu('Moore or Less!?', 1000, 800, theme=pygame_menu.themes.THEME_DARK)            
        self.main_menu.add.text_input('Name :', default=self.player_name, onchange=self.updateName, maxchar=10)
        if self.current_theme == "Light": #If the current theme is light mode, the menu starts on lightmode. This changes if we go to darkmode.
            self.main_menu.add.selector('Theme :', [('Light', 1), ('Dark', 2)], onchange=self.setTheme) 
        else:
            self.main_menu.add.selector('Theme :', [('Dark', 1), ('Light', 2)], onchange=self.setTheme) 
        self.main_menu.add.button('Play', self.startTheGame)
        self.main_menu.add.button('Leaderboard', self.viewLeaderboard)
        self.main_menu.add.button('Quit', pygame_menu.events.EXIT)
        
       
        self.main_menu.mainloop(self.screen)
        pygame.display.flip()
        
    def startTheGame(self):
        '''
        Exits menu and changes mode
        args:None
        return:None
        '''
        
        self.main_menu.disable()
        
        
        #Gets an updated version of player stats and leaderboard upon game start
        with open(self.leaderboard_path) as readfile:
            self.leaderboard = json.load(readfile)
            
        if self.player_name not in self.leaderboard: #If you aren't already in the leaderboard, your name is added
            self.leaderboard.update({self.player_name: self.score})
        
        with open(self.leaderboard_path, 'w') as outfile:
            json.dump(self.leaderboard, outfile)
        self.state = "GAME"
         
         
    def updateName(self, name):
        '''
        When player changes their name, the controller keeps track of that
        args:None
        return:None
        '''
        self.player_name = name
        
    

    def setTheme(self, mode, option):
        '''
        changes the theme between light and dark
        args:self, mode(str), option(Int)
        return:None
        '''
        self.current_theme = mode[0][0]
        if self.current_theme == "Light":
            self.background = pygame.transform.scale(self.light_background, (1000, 800))
            self.main_menu.disable() #Disables current menu, restarts the menu loop with light theme
            self.menuLoop()
        else:
            self.background = pygame.transform.scale(self.dark_background, (1000, 800))
            self.main_menu.disable() #Disables current menu, restarts the menu loop with dark theme
            self.menuLoop()
            
            

    def viewLeaderboard(self):
        '''
        Exits main menu and changes mode to leaderboard
        args:None
        return:None
        '''
        self.main_menu.disable()
        self.state = "LEADERBOARD"
    
    def leaderboardLoop(self):
        '''
        Sets up the leaderboard menu. Accesses leaderboard for most recent scores, sorts the scores, and displays them
        Args: None
        Returns: None
        '''
        if self.current_theme == "Light": #If the theme is light, lightmode is used. Otherwise the dark theme is used.
            self.leaderboard_menu = pygame_menu.Menu("Leaderboard", 1000, 800, theme=pygame_menu.themes.THEME_BLUE)
        else:
            self.leaderboard_menu = pygame_menu.Menu("Leaderboard", 1000, 800, theme=pygame_menu.themes.THEME_DARK)
           
        
        with open(self.leaderboard_path) as readfile: #Updates the current leaderboard
             self.leaderboard = json.load(readfile)

        current_highscores = sorted(self.leaderboard.items(), key=lambda item: item[1], reverse = True )
        for i in range(0,10):
            if i >= len(current_highscores): #Adds filler scores if there is less than 10 people on the leaderboard
                self.leaderboard_menu.add.label(f"{i+1}. Player || SCORE:N/A") 
            else:
                self.leaderboard_menu.add.label(f"{i+1}. {current_highscores[i][0]} || SCORE:{current_highscores[i][1]}") #Adds player scores
        self.leaderboard_menu.add.button("Main Menu", self.goToMenuLeaderboard)
        self.leaderboard_menu.mainloop(self.screen)
        pygame.display.flip()
      
    def goToMenuLeaderboard(self):
        '''
        Exits leaderboard menu and changes mode to main menu
        args:None
        return:None
        '''
        self.leaderboard_menu.disable()
        self.state = "MAIN_MENU"
      
    
        
    def endLoop(self):
        '''
        Sets up the game over menu.
        args:None
        return:None
        '''
        if self.current_theme == "Light":#If the theme is light, lightmode is used. Otherwise the dark theme is used.
            self.end_menu = pygame_menu.Menu('Game Over!', 1000, 800, theme=pygame_menu.themes.THEME_BLUE)
        else:
            self.end_menu = pygame_menu.Menu('Game Over!', 1000, 800, theme=pygame_menu.themes.THEME_DARK)
        self.end_menu.add.label("You lost!")
        self.end_menu.add.label(f"Score:{self.score}")
        self.end_menu.add.label(f"{self.base_name} had {self.base_count} tweets.")
        self.end_menu.add.label(f"{self.comparison_name} had {self.comparison_count} tweets.")
        self.end_menu.add.button('Play again', self.restartTheGame)
        self.end_menu.add.button('Leaderboard', self.viewLeaderboardEnd)
        self.end_menu.add.button('Main Menu', self.goToMenuEnd)
        self.end_menu.add.button('Quit', pygame_menu.events.EXIT)
        
        #resets scores and highscore
        self.score = 0
        self.high_score = 0 
        
        self.end_menu.mainloop(self.screen)
        pygame.display.flip()
        
    def restartTheGame(self):
        '''
        Exits menu and changes mode
        args:None
        return:None
        '''
        self.end_menu.disable()
        self.state = "GAME"
    
    def goToMenuEnd(self):
        '''
        Exits menu and changes mode
        args:None
        return:None
        '''
        self.end_menu.disable()
        self.state = "MAIN_MENU"
        
    def viewLeaderboardEnd(self):
        '''
        Exits menu and changes mode
        args:None
        return:None
        '''
        self.end_menu.disable()
        self.state = "LEADERBOARD"    
        
        



