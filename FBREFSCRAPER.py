import requests
from bs4 import BeautifulSoup
import pandas as pd 
import re
import sys, getopt
import csv

#url = 'https://fbref.com/en/comps/9/passing/Premier-League-Stats'
url = 'https://fbref.com/en/comps/12/La-Liga-Stats'
response = requests.get(url)
#next 2 lines handle issue w comments breaking the parsing process
comm = re.compile("<!--|-->")
soup = BeautifulSoup(comm.sub("",response.text), 'lxml')

#search soup
all_tables = soup.findAll("tbody")
team_table = all_tables[0]
player_table = all_tables[1]
#print(player_table) #(just to show how data is structured)

#setup empty dict
pre_df_player = dict()
features_wanted_player = {"player", "nationality", "position", "squad", "age", "minutes_90s", 
"tackles", "tackles_won", "tackles_def_3rd", "tackles_mid_3rd", "tackles_att_3rd",
"dribble_tackles", "dribbles_vs", "dribble_tackles_pct", "dribbled_past",
 "pressures", "pressure_regains", "pressure_regain_pct", "pressures_def_3rd",
 "pressures_mid_3rd", "pressures_att_3rd", "blocks", "blocked_shots_saves",
 "blocked_passes", "interceptions", "clearances", "errors"}


features_wanted_player2 = {"player", "position", "minutes_90s", "tackles",  
"dribble_tackles_pct", "pressure_regain_pct", "interceptions"}
#features_wanted_play = {"minutes_90s", "tackles_def_3rd"}
player_names = []
count = 0 
#make list of all rows (tr tags)
rows_squad = player_table.find_all('tr')
#loop over rows, find data-stat tag
for row in rows_squad:
    #if(row.find('th',{"scope":"row"}) != None):
        #strip garbarge, leaves simple text
        #name = row.find('th',{"data-stat":"ranker"}).text.strip().encode().decode("utf-8")
        
        #save data to dict (append new value to list w/in dict OR add new key w/ new value)
       # if 'player' in pre_df_player:
            #pre_df_player['player'].append(name)
        #else:
            #pre_df_player['player'] = [name]
    for f in features_wanted_player2:
        if (row.find("td",{"data-stat": f}) != None):
            cell = row.find("td",{"data-stat": f})
            #print(f)
            #print(cell)
            a = cell.text.strip().encode()
            text = a.decode("utf-8")
            if (text == 'FW' or text == 'GK'):
                #do nothing we don't want them
                #skipThis = True
                break
            ###this elseif block is adding the FW and GKs we want excluded
            elif (f != 'player'):
                if f in pre_df_player:
                    pre_df_player[f].append(text)
                else:
                    pre_df_player[f] = [text]
            else:
                #players name
                player_names.append(text)

print(len(player_names))
df_player = pd.DataFrame(pre_df_player, index=player_names)
###ValueError: Shape of passed values is (473, 6), indices imply (363, 6)
###HOWTOFIX:
#print(df_player.head())
df_player.to_csv('RandomShit.csv', encoding='utf-8-sig')

