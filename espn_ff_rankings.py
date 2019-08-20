# -*- coding: utf-8 -*-
"""
Created on Fri Jun  7 16:06:34 2019

@author: William
"""

from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
import pandas as pd

url = 'https://www.espn.com/fantasy/football/story/_/id/25759239/fantasy-football-2019-updated-ppr-rankings-matthew-berry'

client = uReq(url)
page_html = client.read()
page_html
client.close()

page_soup = soup(page_html, 'html.parser')

page_soup
page_soup.prettify()

containers = page_soup.findAll('aside', {'class':'inline inline-table'})


#Removes the first container that doesn't have pertainent info
rankings = containers[1:5]
rankings = rankings[0]


top_200 = rankings.find('tbody')
top_200.text



ranks = []

#Iterates over the rankings and finds all the 'td' tags then extrapolates
#over the text for each individual instance of the text
for information in rankings:
    text = information.find_all('td')
    for info in text:
        print(info.text)
        
        ranks.append(info.text)


all_position_ranks = pd.DataFrame(ranks)
        
#Creates a list of every other line starting at the second line
team_list = all_position_ranks[1::3].reset_index(drop = True)
#Keeps all even rows starting at the first index and resetting the index
position_list = all_position_ranks.iloc[2::3, :].reset_index(drop = True)

player_names = all_position_ranks[0::3].reset_index(drop = True)

#Creates new dataframe and splits based on criteria 
new = position_list[0].str.split('.', n = 1, expand = True)
print(new)


#Merges on the two dataframes based on their index
all_position_ranks = pd.merge(position_list, team_list, left_index = True, right_index = True)

all_position_ranks = all_position_ranks.rename(columns = {'0_x':'position', 
                                                          1:'name', '0_y':'team'})

rank_player_list = player_names[0].str.split('.', n = 1, expand = True)
    
all_position_ranks = pd.merge(rank_player_list, all_position_ranks , left_index = True, right_index = True)
all_position_ranks.columns = ['rank', 'player_names', 'position', 'team']


all_position_ranks.sample(20)
all_position_ranks.info()

all_position_ranks['rank'] = all_position_ranks['rank'].astype(int)
all_position_ranks.info()


matthew_berrys_pos_rank = all_position_ranks

date_info = page_soup.find('span', {'data-dateformat':'date1'})


berry_date_updated = date_info.text
print(berry_date_updated)


matthew_berrys_pos_rank.to_csv('matthew_berrys_top_position_ranks_' + berry_date_updated + '.csv', index = None, header = True)





url2 = 'https://www.espn.com/fantasy/football/story/_/id/26415022/fantasy-football-updated-2019-ppr-rankings-mike-clay'


client = uReq(url2)
page_html = client.read()
page_html
client.close()

page_soup = soup(page_html, 'html.parser')

page_soup

containers = page_soup.findAll('aside', {'class':'inline inline-table'})


containers[1]


top_300 = containers[1].find('tbody')
top_300




clay_300 = []

for text in top_300:
    info = text.find_all('td')
    for td in info:
        print(td.text)
        
        clay_300.append(td.text)

all_300 = pd.DataFrame(clay_300)


team_list = all_300[2::5].reset_index(drop = True).rename(columns = {0:'team'})
position_list = all_300[1::5].reset_index(drop = True).rename(columns = {0:'position'})
bye_week = all_300[3::5].reset_index(drop = True).rename(columns = {0:'bye_week'})
position_rank = all_300[4::5].reset_index(drop = True).rename(columns = {0:'posrank'})
players = all_300[0::5].reset_index(drop = True).rename(columns = {0:'player'})


clays_top_300 = pd.concat([players, position_list, team_list, bye_week, position_rank], axis = 1)

date_info = page_soup.find('span', {'data-dateformat':'date1'})
clay_date_updated = date_info.text

clays_top_300.head(10)

print(clay_date_updated)

clays_top_300.to_csv('clays_top_300_' + clay_date_updated +'.csv', index = None, header = True)
