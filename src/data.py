from os import write
import json 
json_pointer = open("trends.json", "r")
objects = json.load(json_pointer)
objects.pop(0)
objects.pop()


list = [1,2,3,4,5,6,7,8]

class Comparison:
    def __init__(self, base_trend, comparison_trend):
        self.base_trend = base_trend
        self.comparison_trend = comparison_trend
    
    def __str__(self):
        return(f"{self.base_trend}, {self.comparison_trend}")
    
    def CompareTrends(self):
        score = 0
        if objects[self.base_trend][1] > objects[self.comparison_trend][1]:
            score += 1 
        else:
            score = 0 

        return score

c = Comparison(1, 0)
print(str(c))
print(c.CompareTrends())