# Basketball-Reference.com Selenium Web Scraper
Extracts and transforms player data from basketball-reference.com using Selenium and Pandas. 

I made this to have access to players data for some casual exploration & visualization.
Future improvements include making it more useful for others who might want to use it to collect data for themselves, for example for those who want to use their own list of players to scrape data for.  

Player_scrape grabs the gamelog stat data for the entire career of all active players (as listed by basketball-reference.com) and saves them to a csv.
Player_clean removes inactive games and adds labels for sorting.
Activate_players is used by the other two scripts, but will output all active players (as listed by basketball-reference.com). For the 2022-23 season, NBA.com has stats for 539 players in the regular season. Currently, Basketball-reference has 690 players listed as active, so it collects more than just current players. 
