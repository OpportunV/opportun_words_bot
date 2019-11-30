import googletrans as gt
import requests
from bs4 import BeautifulSoup

from typing import List

from config import id_white_list


class RandomUrban:
    def __init__(self):
        url = 'https://www.urbandictionary.com/random.php?page=1'
        r = requests.get(url)
    
        soup = BeautifulSoup(r.content, 'html5lib')
        top_def = soup.find('div', class_='def-panel')
        
        word = top_def.find('a', class_='word')
        
        self.link = 'https://www.urbandictionary.com{}'.format(word.attrs.get('href'))
        self.word = word.text
        self.meaning = top_def.find('div', class_='meaning').text
        self.example = top_def.find('div', class_='example').text
        

def dict_meanings(word: str) -> List[str]:
    return ['']


def translate(phrase: str, source='en', target='ru') -> List[str]:
    return ['']


def add(user_id: int, word: str, meaning: str) -> None:
    if user_id not in id_white_list:
        return None
    
    return None


def delete(user_id: int, word: str) -> None:
    pass


def for_test():
    pass
    

def main():
    urban = RandomUrban()
    print(f"{urban.word}\n{urban.link}\n\n{urban.meaning}\n\n{urban.example}")
    

if __name__ == '__main__':
    main()
