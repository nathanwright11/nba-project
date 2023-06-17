from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from time import sleep, time
import csv

from active_players import get_active_players


def get_seasons_active(player_url):
    """Returns list of seasons player was active"""
    chromedriver_path = '/usr/bin/chromedriver'
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--blink-settings=imagesEnabled=false')
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument('--disable-gpu')
    service = Service(chromedriver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    driver.get(player_url)
    table = driver.find_element(By.ID, 'per_game')
    seasons = [th.text for th in table.find_elements(By.XPATH, './/tbody/tr/th')]
    driver.quit()
    return list(set(seasons))


def get_gamelog(player_url, season, i):
    """Makes API request for current season then scrapes game stats"""
    games = []
    driver.get(player_url[:-5] 
               + "/gamelog/" 
               + str(int(season[:4])+1)
               )
    
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
    return headers, games


def save_gamelog(player_url, headers, games, i):
    """Adds game stats from current season to player csv"""
    name = player_url.split('/')[-1].split('.')[0]
    if i == 0:
        with open(f'stats/{name}_games.csv', 'w', newline="") as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            f.close()
    for game in games:
        with open(f'stats/{name}_games.csv', 'a', newline="") as f:
            writer = csv.writer(f)
            writer.writerow(game)
            f.close()


if __name__ == '__main__':
    chromedriver_path = '/usr/bin/chromedriver'
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--blink-settings=imagesEnabled=false')
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument('--disable-gpu')
    
    players = get_active_players()
    for player, url in players.items():
        service = Service(chromedriver_path)
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        seasons = get_seasons_active(url)
        req_count = 1
        beg = time()
        for i, season in enumerate(seasons):
            if (time() - beg) > 60:
                beg = time()
                req_count = 0
            if req_count == 20:
                wait = 65 - (time() - beg)
                print(f"Request limit reached. Wait {wait:.2f} seconds")
                sleep(wait)
            headers, games = get_gamelog(url, season, i)
            save_gamelog(url, headers, games, i)
            req_count += 1
        print(f'{player} games saved')
        driver.quit()