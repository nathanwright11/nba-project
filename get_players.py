from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from string import ascii_lowercase
from unidecode import unidecode
from time import sleep
from re import sub


def get_players(players):
    """Returns a dict of chosen players and their urls, or all active players.
    
    1. Accepts 'active' as argument which grabs all active players
    2. If a list is given, grabs all players in the list
    Format: get_players('active') 
        OR  get_players(['Kobe Bryant', 'Lebron James', 'Steph Curry', etc.])
    """
    chromedriver_path = '/usr/bin/chromedriver'
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--blink-settings=imagesEnabled=false')
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument('--disable-gpu')
    service = Service(chromedriver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    player_list_url = "https://www.basketball-reference.com/players/"
    players_dict = {}

    if players == 'active':
        for i, letter in enumerate(list(ascii_lowercase)):
            if i == 15:
                print(f"Request limit reached. 65 second timeout")
                sleep(65)
            if letter == 'x':
                try:
                    driver.get(player_list_url+letter)
                except:
                    continue
            driver.get(player_list_url+letter)
            table = driver.find_element(By.ID, 'players')
            bold_names = table.find_elements(By.CSS_SELECTOR, 'strong')
            for name in bold_names:
                player = name.text
                url = name.find_element(By.TAG_NAME, 'a').get_attribute('href')
                players_dict[player] = url
                print(f'{player} url saved')
    else:
        players = [player.lower() for player in players]
        player_last = [player.split()[1][0] for player in players]
        player_letter = list(set(player_last))
        for letter in player_letter:
            driver.get(player_list_url+letter)
            table = driver.find_element(By.ID, 'players')
            p_list = [th for th in table.find_elements(By.XPATH, './/tbody/tr/th')]
            for p in p_list:
                if unidecode(sub(r'\*', '', p.text)).lower() in players:
                    name = sub(r'\*', '', p.text)
                    url = p.find_element(By.TAG_NAME, 'a').get_attribute('href')
                    players_dict[name] = url
                    print(f'{name} url saved')
    driver.quit()
    return players_dict


if __name__ == '__main__':
    players = get_players('active')
    print(players)