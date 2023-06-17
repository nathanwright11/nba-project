# nba-project
Extracts and transforms player data from basketball-reference.com using Selenium and Pandas. 

Player_scrape grabs the gamelog stat data for the entire career of all active players (as listed by basketball-reference.com) and saves them to a csv.
Player_clean removes inactive games and adds labels for sorting.
Activate_players is used by the other two scripts, but will output all active players (as listed by bbref.com).

For the 2022-23 seasons, NBA.com has stats for 539 players in the regular season. Basketball-reference has 690 listed as active, so you will be getting more than just current players. 
