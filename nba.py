from urllib.request import urlopen
from bs4 import BeautifulSoup
import json
import pandas as pd
import string
import os

class get_player_code:
    def __call__(self,url):
        player_codes=[]
        html=urlopen(url).read().decode('utf-8')
        nba_players=json.loads(html)['payload']['players']
        for player_code in nba_players:
            player_codes.append(player_code['playerProfile']['code'])
        return player_codes
class creat_player_list:
    years=['2000-2009','2010-2013']                                    #填入退役球員的年份範圍
    alphabets=list(string.ascii_uppercase)
    job_players_url='https://china.nba.com/static/data/league/playerlist.json'
    retire_players_url='https://china.nba.com/static/data/league/historicalplayerlist_{alphabets}_{years}.json'
    def job_players(self):
        job_player_list=get_player_code()
        return job_player_list(self.job_players_url)
    def retire_players(self):
        retire_player_list_group=[]
        retire_player_list=get_player_code()
        for year in self.years:
            for alphabet in self.alphabets:
                retire_player_list_group.extend(retire_player_list(self.retire_players_url.format(alphabets=alphabet,years=year)))
        return retire_player_list_group
class get_player_data:
    job_players_url='https://china.nba.com/static/data/player/stats_{player}.json'
    retire_players_url='https://china.nba.com/static/data/player/historicalstats_{player}.json'
    finish_player=list(map(lambda x : x[0:-5] ,os.listdir("nba_player/")))
    def job_player(self,player):
        player_eachyear_list=[]
        try:
            html=urlopen(self.job_players_url.format(player=player)).read().decode('utf-8')
        except:
            print(player)                                              #打印未能爬最球員的名字
            return True
        nba_player=json.loads(html)
        player_name=nba_player['payload']['player']['playerProfile']['displayName']
        player_position=nba_player['payload']['player']['playerProfile']['position']
        player_weight=nba_player['payload']['player']['playerProfile']['weight']
        player_height=nba_player['payload']['player']['playerProfile']['height']
        player_draftYear=nba_player['payload']['player']['playerProfile']['draftYear']
        for each_yearteam_data in nba_player['payload']['player']['stats']['regularSeasonStat']['playerTeams']:
            player={}
            player.update({'season':each_yearteam_data['season'],
                           #'teamname':each_yearteam_data['profile']['name'],
                           'displayName':player_name,
                           'position':player_position,
                           'weight':player_weight,
                           'height':player_height,
                           'draftYear':player_draftYear})
            player.update(each_yearteam_data['statAverage'])
            player.update(each_yearteam_data['statTotal'])
            player_eachyear_list.append(player)
        return player_eachyear_list
    def retire_player(self,player):
        player_eachyear_list=[]
        try:
            html=urlopen(self.retire_players_url.format(player=player)).read().decode('utf-8')
        except:
            print(player)                                              #打印未能爬最球員的名字
            return True
        nba_player=json.loads(html)
        player_name=nba_player['payload']['player']['playerProfile']['displayName']
        player_position=nba_player['payload']['player']['playerProfile']['position']
        player_weight=nba_player['payload']['player']['playerProfile']['weight']
        player_height=nba_player['payload']['player']['playerProfile']['height']
        player_draftYear=nba_player['payload']['player']['playerProfile']['draftYear']
        for each_yearteam_data in nba_player['payload']['player']['stats']['regularSeasonStat']['playerTeams']:
            #break
            player={}
            player.update({'season':each_yearteam_data['season'],
                           #'teamname':each_yearteam_data['profile']['name'],
                           'displayName':player_name,
                           'position':player_position,
                           'weight':player_weight,
                           'height':player_height,
                           'draftYear':player_draftYear})
            player.update(each_yearteam_data['statAverage'])
            player.update(each_yearteam_data['statTotal'])
            player_eachyear_list.append(player)
        return player_eachyear_list
class creat_player_data_json():
    player_list=creat_player_list()
    job_player_list=player_list.job_players()
    retire_player_list=player_list.retire_players()
    job_player_list_finish=list(map(lambda x : x[0:-5] ,os.listdir("nba_player/job")))
    retire_player_list_finish=list(map(lambda x : x[0:-5] ,os.listdir("nba_player/retire")))
    job_player_list=list(set(job_player_list).difference(set(job_player_list_finish)))
    retire_player_list=list(set(retire_player_list).difference(set(retire_player_list_finish)))
    creep_web=get_player_data()
    def job_player(self):
        for job_player in self.job_player_list:
            player_data=self.creep_web.job_player(job_player)
            if player_data:
                continue
            with open('nba_player/job/{player}.json'.format(player=job_player), 'w') as fp:  #以json存放在nba_player/job/
                json.dump(player_data, fp)
    def retire_player(self):
        for retire_player in self.retire_player_list:
            player_data=self.creep_web.retire_player(retire_player)
            if player_data:
                continue
            with open('nba_player/retire/{player}.json'.format(player=retire_player), 'w') as fp:  #以json存放在nba_player/retire/
                json.dump(player_data, fp)
            
if __name__=='__main__':
    playera=creat_player_data_json()
    playera.job_player()
    playera.retire_player()
