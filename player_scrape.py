from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import csv


def get_seasons_active(first, last):
    """Returns list of seasons player was active"""
    driver.get(player_url 
               + f"{last[:1]}/{last[:5]}{first[:2]}01.html")
    
    table = driver.find_element(By.ID, 'per_game')
    seasons = [th.text for th in table.find_elements(By.XPATH, './/tbody/tr/th')]

    return list(set(seasons))


def save_season_games(first, last, type, flag):
    """Scrapes and saves games stats for a single season.
    
    Gets regular and playoff (if applicable) game stats, then adds those stats
    to separate regular and playoff csv. 
    """
    if type == 'regular':
        type_id = 'pgl_basic'

    elif type == 'playoff':
        type_id = 'pgl_basic_playoffs'

    if type == 'playoff':
        try:
            table = driver.find_element(By.ID, type_id)
        except:
            return
    
    table = driver.find_element(By.ID, type_id)
    headers = [th.text for th in table.find_elements(By.XPATH, './/thead/tr/th')]
    headers.remove('Rk')       #  Rank data ignored in game stat scraping

    games = []
    for row in table.find_elements(By.XPATH, './/tbody/tr'):
        row_data = [td.text for td in row.find_elements(By.XPATH, './/td')]
        if row_data:
            games.append(row_data)

    if flag == 0:
        with open(f'stats/{last[:5]}{first[:2]}_{type}_games.csv', 'w', newline="") as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            f.close()

    for game in games:
        with open(f'stats/{last[:5]}{first[:2]}_{type}_games.csv', 'a', newline="") as f:
            writer = csv.writer(f)
            writer.writerow(game)
            f.close()


def get_career_games(player):
    """Creates the URLs for each season the player was active and saves the game data 
    """
    first, last = player.split()
    seasons = get_seasons_active(first, last)
    _ = 0       #  Temp variable used to add csv header on first iteration only
    for season in seasons:
        driver.get(player_url 
                   + f"{last[:1]}/{last[:5]}{first[:2]}01/gamelog/" 
                   + str(int(season[:4])+1))

        time.sleep(2)

        save_season_games(first, last, 'regular', _)
        save_season_games(first, last, 'playoff', _)

        _ += 1

    print(f"{last} scrape: success")


players = ['stephen curry',
           'lebron james',
           'jayson tatum',
           'jimmy butler', 
           'nikola jokic',
           'kevin durant',
           'joel embiid',
           'giannis antetokounmpo']

player_url = "https://www.basketball-reference.com/players/"

chromedriver_path = '/usr/bin/chromedriver'

chrome_options = Options()
chrome_options.add_argument('--headless')

service = Service(chromedriver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

for player in players:
    get_career_games(player)

driver.quit()