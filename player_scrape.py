from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from time import sleep
import csv

from active_players import get_active_players


def get_seasons_active(player):
    """Returns list of seasons player was active"""
    chromedriver_path = '/usr/bin/chromedriver'
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--blink-settings=imagesEnabled=false')
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument('--disable-gpu')
    service = Service(chromedriver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    player_url = "https://www.basketball-reference.com/players/"
    first, last = player.lower().split()
    driver.get(player_url 
               + f"{last[:1]}/{last[:5]}{first[:2]}01.html"
               )
    table = driver.find_element(By.ID, 'per_game')
    seasons = [th.text for th in table.find_elements(By.XPATH, './/tbody/tr/th')]
    driver.quit()
    return list(set(seasons))


def get_gamelog(player, season, i):
    """Makes API request for current season then scrapes game stats"""
    player_url = "https://www.basketball-reference.com/players/"
    first, last = player.lower().split()
    games = []
    driver.get(player_url 
               + f"{last[:1]}/{last[:5]}{first[:2]}01/gamelog/" 
               + str(int(season[:4])+1)
               )
    sleep(2)     #Avoids more than 20 API reqs per min
    
    r_table = driver.find_element(By.ID, 'pgl_basic')
    for row in r_table.find_elements(By.XPATH, './/tbody/tr'):
        row_data = [td.text for td in row.find_elements(By.XPATH, './/td')]
        row_data.append('Regular')
        if row_data:
            games.append(row_data)
            
    if driver.find_elements(By.ID, 'pgl_basic_playoffs'):
        p_table = driver.find_element(By.ID, 'pgl_basic_playoffs')
        for row in p_table.find_elements(By.XPATH, './/tbody/tr'):
            row_data = [td.text for td in row.find_elements(By.XPATH, './/td')]
            row_data.append('Playoffs')
            if row_data:
                games.append(row_data)

    if i == 0:
        headers = [th.text for th in r_table.find_elements(By.XPATH, './/thead/tr/th')]
        headers.remove('Rk')       #  Rank data ignored in game stat scraping
        headers.append('Type')
    else:
        headers = []

    print(f'{last} {season} scrape success')
    return headers, games


def save_gamelog(player, headers, games, i):
    """Adds game stats from current season to player csv"""
    first, last = player.lower().split()
    if i == 0:
        with open(f'stats/{last[:5]}{first[:2]}_games.csv', 'w', newline="") as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            f.close()
    for game in games:
        with open(f'stats/{last[:5]}{first[:2]}_games.csv', 'a', newline="") as f:
            writer = csv.writer(f)
            writer.writerow(game)
            f.close()
    print(f'games saved')


if __name__ == '__main__':
    chromedriver_path = '/usr/bin/chromedriver'
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--blink-settings=imagesEnabled=false')
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument('--disable-gpu')
    
    players = ['Stephen Curry',
        'Lebron James',
        'Jayson Tatum',
        'Jimmy Butler', 
        'Nikola Jokic',
        'Kevin Durant',
        'Joel Embiid',
        'Giannis Antetokounmpo'
        ]
    #players = get_active_players()
    for player in players:
        service = Service(chromedriver_path)
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        seasons = get_seasons_active(player)
        #headers, games = get_career_games(player, seasons)
        for i, season in enumerate(seasons):
            headers, games = get_gamelog(player, season, i)
            save_gamelog(player, headers, games, i)

        driver.quit()