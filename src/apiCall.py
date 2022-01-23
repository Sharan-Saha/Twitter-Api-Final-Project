import json
from pathlib import Path
import requests
#You can access apiCodes.py by unzipping the Codes.zip file, ask me(Senih) for the password

class ApiCall:

    
    def __init__(self):
        '''
        Initializes parameters
        Parameters: None
        Returns:None
        '''
        self.url = "https://moore-or-less.herokuapp.com/api/twitter/"

        
    def getTrends(self):
        '''
        Checks to see if trends.json exists. If it does, it reads the data in the file. If the file doesn't exist, it creates a trends.json file and and dumps the most up to date trends list into the newly created file
        Parameters: None
        Returns: None

        '''
        self.trends = (requests.get(self.url)).text
        self.trends = eval(self.trends)
        self.path = Path('src/trends.json')
        if self.path.is_file():
            with open(self.path, "w") as outfile:
                json.dump(self.trends, outfile)        
        
        print(self.trends)
        print(type(self.trends))

