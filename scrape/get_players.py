import re
import time

from bs4 import BeautifulSoup
import requests
from string import ascii_lowercase
from unidecode import unidecode


def get_players(players):
    """Returns a dict of chosen players and their urls, or all active players.
    
    1. Accepts 'active' as argument which grabs all active players
    2. If a list is given, grabs all players in the list
    Format: get_players('active') 
        OR  get_players(['Kobe Bryant', 'Lebron James', 'Stephen Curry', etc.])
    """
    player_list_url = "https://www.basketball-reference.com/players/"
    players_dict = {}
    if players == 'active':
        for i, letter in enumerate(list(ascii_lowercase)):
            if (i % 13) == 0 and i != 0:
                print("Request limit reached. 90 second timeout")
                time.sleep(90)
            if letter == 'x':
                try:
                    requests.get(player_list_url+letter)
                except:
                    continue
            r = requests.get(player_list_url+letter)
            soup = BeautifulSoup(r.text, 'html.parser')
            table = soup.find('table', id='players')
            bold_names = table.tbody.select('strong a')
            for name in bold_names:
                player = name.get_text()
                url = name.get('href')
                players_dict[player] = url
                print(f'{player} url saved')
    else:
        players = [player.lower() for player in players]
        player_last = [player.split()[1][0] for player in players]
        player_letter = list(set(player_last))
        for i, letter in enumerate(player_letter):
            if (i % 13) == 0 and i != 0:
                print("Request limit reached. 90 second timeout")
                time.sleep(90)
            r = requests.get(player_list_url+letter)
            soup = BeautifulSoup(r.text, 'html.parser')
            table = soup.find('table', id='players')
            p_list = [th for th in table.tbody.find_all('th')]
            for p in p_list:
                if unidecode(re.sub(r'\*', '', p.get_text())).lower() in players:
                    name = re.sub(r'\*', '', p.get_text())
                    url = p.a.get('href')
                    players_dict[name] = url
                    print(f'{name} url saved')
    return players_dict


if __name__ == '__main__':
    players = get_players('active')
    print(players)