import json
from typing import Dict


class Destinations:
    def __init__(self, filename='destinations.json'):
        self.filename = filename
        
    def get(self):
        with open(self.filename) as f:
            destinations: list = json.load(f)
        return destinations
    
    def update(self, new):
        with open(self.filename, 'w') as f:
            json.dump(new, f)

    def add(self, destination: int) -> bool:
        destinations = self.get()
        
        if destination in destinations:
            return False
    
        destinations.append(destination)
        
        self.update(destinations)
        return True

    def remove(self, destination: int) -> bool:
        destinations = self.get()
    
        if destination not in destinations:
            return False
    
        destinations.remove(destination)
    
        self.update(destinations)
        return True
    

def get_replies(filename: str = 'replies.json') -> Dict:
    with open(filename) as f:
        return json.load(f)








