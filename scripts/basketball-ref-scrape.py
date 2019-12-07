# Scraping Basketball-reference.com
import requests
import csv
import pandas as pd
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

# Print out each player in single game dicitonary
def print_by_players(player_list):
    for entry in player_list:
        for key in entry.keys():
            print("--- " + key + " ---")
            for stat in entry[key].keys():
                print(stat + ": " + entry[key][stat])
            print("\n")

# Takes single game box-score url and returns list of player stat dictionaries
def scrape_single_game_player_stats(url):
    game_soup = create_page_soup(url) # creates soup object for passed url
    boxscore_table = game_soup.find_all('table',{'id':'box-NYK-game-basic'})
    boxscore_table_body = boxscore_table[0].find_all('tbody')
    boxscore_rows = boxscore_table_body[0].find_all('tr') # rows containing player stats
    player_game_stats = [] # list to hold stat dictionary associated with each player

    for i in range(len(boxscore_rows)):
        if i == 5:
            continue # row that divides starters and bench
        player_stats = {}
        player_head = boxscore_rows[i].find_all('th')
        player_name = player_head[0]['csk']
        player_data = boxscore_rows[i].find_all('td')

        for stat in player_data:
            player_stats[stat['data-stat']] = stat.get_text()

        full_player = {player_name: player_stats}
        player_game_stats.append(full_player)

    return player_game_stats

# Get team totals for a single boxscore
def scrape_single_game_totals(url):
    totals_dict = {}
    game_soup = create_page_soup(url)
    boxscore_table = game_soup.find_all('table',{'id':'box-NYK-game-basic'})
    boxscore_footer = boxscore_table[0].find_all('tfoot')
    footer_row = boxscore_footer[0].find_all('tr')
    footer_data = footer_row[0].find_all('td')

    for stat in footer_data:
        totals_dict[stat['data-stat']] = stat.get_text()

    return totals_dict


# -------- MAIN ---------
#test_dict = initialize_boxscore_dict()
player_stats = scrape_single_game_player_stats('https://www.basketball-reference.com/boxscores/201910230SAS.html')
#test_total = scrape_single_game_totals('https://www.basketball-reference.com/boxscores/201910230SAS.html')

#test_df = pd.DataFrame(player_stats[0])
test_df = pd.DataFrame()
player_name = player_stats[1].keys()[0]
stat_names = []

for stat in player_stats[1][player_name].keys():
    stat_names.append(stat)
test_df.insert(0,"Stat",stat_names)

for i in range(0,len(player_stats) - 1):
    stat_list = []
    player_name = player_stats[i].keys()[0]
    for val in player_stats[i][player_name].values():
        stat_list.append(val)
    try:
        test_df.insert(i + 1,player_name,stat_list)
    except ValueError:
        break

print(test_df.head(5))
