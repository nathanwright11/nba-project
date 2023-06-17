from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from string import ascii_lowercase
from time import sleep, time


def get_active_players():
    """Returns a dictionary of all active players and their urls."""
    chromedriver_path = '/usr/bin/chromedriver'
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--blink-settings=imagesEnabled=false')
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument('--disable-gpu')
    service = Service(chromedriver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    player_list_url = "https://www.basketball-reference.com/players/"
    players = {}
    req_count = 0
    req_limit = 15
    req_window = 65
    for letter in list(ascii_lowercase):
        if req_count == req_limit:
            print(f"Request limit reached. {req_window} second timeout")
            sleep(req_window + 5)
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
            players[player] = url
        req_count += 1
        print(f'{letter} scraped')
    driver.quit()
    return players


if __name__ == '__main__':
    players = get_active_players()
    print(players)