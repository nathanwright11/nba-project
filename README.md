# Basketball-Reference.com requests/bs4 Web Scraper
Extracts and transforms player data from basketball-reference.com using requests, BeautifulSoup, and pandas. Capable of either getting the career games of all active players, or only the career games of players in a list. Cleaning the games removes all games not played, and sorts game by date. Heads up, grabbing the career game stats of all active players takes around 7-8 hours.

As an NBA fan, I made this to have access to players' data for some casual exploration & visualization. Basketball-reference has stated they are okay with web scraping, as long as there are no more than 20 requests per minute, as of today. If you break this rule, they will lock you out for 1 hour. In the past, I have been locked out for between 15-20 requests, so this function keeps it to lucky number 13, and then waits 90 seconds to avoid being locked out by bbref. I was able to scrape all active players' games stats using this method. 
BBref data scraping policy: https://www.sports-reference.com/bot-traffic.html

Future improvements include adding option to choose seasons to scrape, and an option to scrape Hall of Fame players.
