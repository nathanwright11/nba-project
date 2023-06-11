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


def get_career_games(player, seasons):
    """Scrapes and returns regular and playoff games stats of entire career."""
    chromedriver_path = '/usr/bin/chromedriver'
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    service = Service(chromedriver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    _ = 0       #  Temp variable grabs csv header on first iteration only
    player_url = "https://www.basketball-reference.com/players/"
    first, last = player.lower().split()
    r_games = []
    p_games = []
    for season in seasons:
        driver.get(player_url 
                   + f"{last[:1]}/{last[:5]}{first[:2]}01/gamelog/" 
                   + str(int(season[:4])+1)
                   )
        sleep(2)     #Avoids more than 20 API reqs per min
        
        r_table = driver.find_element(By.ID, 'pgl_basic')
        for row in r_table.find_elements(By.XPATH, './/tbody/tr'):
            row_data = [td.text for td in row.find_elements(By.XPATH, './/td')]
            if row_data:
                r_games.append(row_data)
                
        if driver.find_elements(By.ID, 'pgl_basic_playoffs'):
            p_table = driver.find_element(By.ID, 'pgl_basic_playoffs')
            for row in p_table.find_elements(By.XPATH, './/tbody/tr'):
                row_data = [td.text for td in row.find_elements(By.XPATH, './/td')]
                if row_data:
                    p_games.append(row_data)

        if _ == 0:
            head = [th.text for th in r_table.find_elements(By.XPATH, './/thead/tr/th')]
            head.remove('Rk')       #  Rank data ignored in game stat scraping
        _ += 1
    driver.quit()
    print(f'{last} scrape success')
    return head, r_games, p_games


def save_career_games(player, header, regular_games, playoff_games):
    """Creates separate csv for regular and playoff career games"""
    first, last = player.lower().split()
    r_path = f'stats/{last[:5]}{first[:2]}_regular_games.csv'
    p_path = f'stats/{last[:5]}{first[:2]}_playoff_games.csv'
    
    with open(r_path, 'w', newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        f.close()
    for game in regular_games:
        with open(r_path, 'a', newline="") as f:
            writer = csv.writer(f)
            writer.writerow(game)
            f.close()
    if playoff_games:
        with open(p_path, 'w', newline="") as f:
            writer = csv.writer(f)
            writer.writerow(header)
            f.close()
        for game in playoff_games:
            with open(p_path, 'a', newline="") as f:
                writer = csv.writer(f)
                writer.writerow(game)
                f.close()
    print(f'{last} csv created')


if __name__ == '__main__':
    players = get_active_players()
    for player in players:
        seasons = get_seasons_active(player)
        head, r_games, p_games = get_career_games(player, seasons)
        save_career_games(player, head, r_games, p_games)