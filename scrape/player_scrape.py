import csv
import os
import time

from bs4 import BeautifulSoup, Comment
import requests

from api_request_limiter import api_req_lmtr
from get_players import get_players


@api_req_lmtr(req_limit=13, wait=90)
def get_seasons_active(player_url):
    """Returns list of seasons player was active."""
    r = requests.get('https://www.basketball-reference.com' 
                     + player_url)
    soup = BeautifulSoup(r.text, 'html.parser')
    table = soup.find('table', id='per_game')
    seasons = [th.get_text() for th in table.tbody.select('th[data-stat="season"]')]
    return list(set(seasons))


@api_req_lmtr(req_limit=13, wait=90)
def get_gamelog(player_url, season, i):
    """Makes API request for current season then scrapes game stats.
    
    Only saves header on first iteration, also adds season type label (regular or
    playoffs). Playoffs data is commented out of the HTML, so had to jump through
    extra hoops to grab it.
    """
    games = []
    r = requests.get('https://www.basketball-reference.com'
                    + player_url[:-5]
                    + '/gamelog/'
                    + str(int(season[:4])+1))
    soup = BeautifulSoup(r.text, 'html.parser')
    table = soup.find('table', id='pgl_basic')
    if i == 0:
        headers = [header.get_text() for header in table.thead.find_all('th')]
        headers.remove('Rk')       #  Rank data ignored in game stat scraping
        headers.append('Type')
    else:
        headers = []
    r_games = table.tbody.select('[id*=pgl_basic]')
    for game in r_games:
        stats = [stat.get_text() for stat in game.find_all('td')]
        stats.append('Regular')
        games.append(stats)
    if soup.find(string=lambda text: isinstance(text, Comment) and '<tab' in text):
        c = soup.find(string=lambda text: isinstance(text, Comment) and '<tab' in text)
        comment_html = BeautifulSoup(c, 'html.parser')
        p_table = comment_html.find('table')
        p_games = p_table.tbody.select('[id*=pgl_basic_playoffs]')
        for game in p_games:
            stats = [stat.get_text() for stat in game.find_all('td')]
            stats.append('Playoffs')
            games.append(stats)
    return headers, games


def save_gamelog(player_url, headers, games, i):
    """Saves game stats from current season to player csv in stats folder."""
    name = player_url.split('/')[-1].split('.')[0]
    folder = '../stats'
    player_file = os.path.join(folder, f'{name}_games.csv')
    if not os.path.exists(folder):
        os.makedirs(folder)
    
    if i == 0:
        with open(player_file, 'w', newline="") as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            f.close()
    for game in games:
        with open(player_file, 'a', newline="") as f:
            writer = csv.writer(f)
            writer.writerow(game)
            f.close()


if __name__ == '__main__':
    players = get_players(['Kobe Bryant', 'Lebron James', 'Stephen Curry',])
    print('90 second timeout')
    time.sleep(90)
    for player, url in players.items():
        seasons = get_seasons_active(url)
        print(f'{player} {len(seasons)} seasons to scrape')
        for i, season in enumerate(seasons):
            headers, games = get_gamelog(url, season, i)
            save_gamelog(url, headers, games, i)
        print(f'{player} games saved')