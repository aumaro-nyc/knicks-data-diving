# Scraping Basketball-reference.com
import requests
from bs4 import BeautifulSoup

url = 'https://www.basketball-reference.com/teams/NYK/2020_games.html'
prefix = 'https://www.basketball-reference.com'

webpage_request = requests.get(url, timeout=5)
webpage = webpage_request.content

soup = BeautifulSoup(webpage, 'html.parser')

dated_boxscores = {}
game_rows = soup.find_all('tr')
scores = soup.find_all('td',{'class': 'center', 'data-stat': 'box_score_text'})
dates = soup.find_all('td',{'class': 'left', 'data-stat': 'date_game'})

# Populate Dated Boxscore dictionary
for i in range(len(dates)):
    link = scores[i].find('a')
    dated_boxscores[dates[i]['csk']] = prefix + link['href']

# Takes a url as an argument and returns a BeautifulSoup object associated w/ url
def create_page_soup(url):
    web_request = requests.get(url, timeout=5)
    soup_object = BeautifulSoup(web_request.content, 'html.parser')
    return soup_object

# Scrapes all boxscore and date information and returns dictionary of date/url pairs
def initialize_boxscore_dict():
    url = 'https://www.basketball-reference.com/teams/NYK/2020_games.html'
    prefix = 'https://www.basketball-reference.com'

    webpage_request = requests.get(url, timeout=5)
    webpage = webpage_request.content

    soup = BeautifulSoup(webpage, 'html.parser')

    dated_boxscores = {}
    game_rows = soup.find_all('tr')
    scores = soup.find_all('td',{'class': 'center', 'data-stat': 'box_score_text'})
    dates = soup.find_all('td',{'class': 'left', 'data-stat': 'date_game'})

    # Populate Dated Boxscore dictionary
    for i in range(len(dates)):
        link = scores[i].find('a')
        dated_boxscores[dates[i]['csk']] = prefix + link['href']

    return dated_boxscores
