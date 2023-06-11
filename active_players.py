from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from string import ascii_lowercase
from time import sleep


def get_active_players():
    """Returns list of all active players"""
    chromedriver_path = '/usr/bin/chromedriver'
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    service = Service(chromedriver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    player_url = "https://www.basketball-reference.com/players/"
    active_players = []
    for x in list(ascii_lowercase):
        try:
            driver.get(player_url+x)
        except:
            continue
        driver.get(player_url+x)
        sleep(8)       #Avoids sending more than 20 API reqs per min
        table = driver.find_element(By.ID, 'players')
        bold_names = table.find_elements(By.TAG_NAME, 'strong')
        players = [name.text for name in bold_names]
        for player in players:
            active_players.append(player)
    driver.quit()
    return active_players


if __name__ == '__main__':
    players = get_active_players()
    print(players)