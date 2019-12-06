# Scraping Basketball-reference.com
import requests
import csv
from bs4 import BeautifulSoup

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

# Write dictionary to csv output file: Pass a dictionary and a path name
def write_dict_to_file(dict, filename):
    with open(filename, 'w') as file:
        for key in dict.keys():
            file.write('%s,%s\n'%(key,dict[key]))

# Create a dictionary from a csv file
def create_dict_from_csv(filename):
    with open(filename, 'r') as inputFile:
        reader = csv.reader(inputFile)
        new_dict = {rows[0]:rows[1] for rows in reader}
        return new_dict

# -------- MAIN ---------
test_dict = initialize_boxscore_dict()

test_url = 'https://www.basketball-reference.com/boxscores/201910230SAS.html'
game_soup = create_page_soup(test_url)

boxscore_table = game_soup.find_all('table',{'id':'box-NYK-game-basic'})
boxscore_table_body = boxscore_table[0].find_all('tbody')
boxscore_rows = boxscore_table_body[0].find_all('tr')
player_game_stats = []

for i in range(len(boxscore_rows)):
    if i == 5:
        continue
    player_stats = {}
    player_head = boxscore_rows[i].find_all('th')
    player_name = player_head[0]['csk']
    player_data = boxscore_rows[i].find_all('td')

    for stat in player_data:
        player_stats[stat['data-stat']] = stat.get_text()

    full_player = {player_name: player_stats}
    player_game_stats.append(full_player)

for entry in player_game_stats:
    print(entry)
