from os import write
import json 
import random
from random import choice
json_pointer = open("trends.json", "r")
deck = json.load(json_pointer)
deck.pop(0)
deck.pop()




class Comparison:
    def __init__(self, base_trend, comparison_trend):
        self.base_trend = base_trend
        self.comparison_trend = comparison_trend
    
    def __str__(self):
        return(f"{self.base_trend}, {self.comparison_trend}")
    
    def CompareTrends(self):
        score = 0
        if deck[self.base_trend][1] > deck[self.comparison_trend][1]:
            score += 1 
        else:
            score = 0 

        return score

# for item_pair in deck:
#     if "Giants" in item_pair:
#         print("True")


base_number = random.randrange(1, len(deck))
comparison_number = random.randrange(1, len(deck))

same_number = False
if base_number == comparison_number:
    same_number = True

while (same_number == True):
    comparison_number = random.randrange(1, len(deck))
    if comparison_number == base_number:
        same_number = False

base = deck[base_number][0]
comparison = deck[comparison_number][0]
        
print(f"Which one do you think is more popular, {base} or {comparison}? ")
