import random

class OddEven:
    
    def __init__(self):
        self.number = 0

    def odd_or_even(self):
        '''
        Generates a 1 or 2
        
        '''
        self.number = random.randrange(1,3)
        #returns either 1 or 2
        return int(self.number)
    
