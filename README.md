# Basketball-Reference.com requests/bs4 Web Scraper
Extracts and transforms player data from basketball-reference.com using requests, BeautifulSoup, and pandas. Can choose to either get the games of all active players, or only the games of players in a list.

I made this to have access to players' data for some casual exploration & visualization.
Future improvements include using requests instead of selenium.

Basketball-reference has stated they are okay with web scraping, as long as there are no more than 20 requests per minute, as of today. If you break this rule, they will lock you out for 1 hour. In the past, I have been locked out for between 15-20 requests, so this function keeps it to lucky number 13, and then waits a little more than the required time to avoid any clock discrepancies. 
BBref data scraping policy: https://www.sports-reference.com/bot-traffic.html