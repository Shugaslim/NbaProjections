import csv
import pandas as pd
import math
from nba_api.stats.endpoints import TeamYearByYearStats
from nba_api.stats.endpoints import TeamEstimatedMetrics
from nba_api.stats.static import teams

class dataExtractor:
    dates = [2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 
                2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022]
    def __init__(self):
        pass

    def getHistoricalData(self):
        
        allteams = teams.get_teams()
        main_df = pd.DataFrame(columns=['TEAM_ID', 'TEAM_CITY', 'TEAM_NAME', 'YEAR', 'GP', 'WINS', 'LOSSES', 'WIN_PCT', 'CONF_RANK', 'DIV_RANK', 'PO_WINS', 'PO_LOSSES', 'CONF_COUNT', 'DIV_COUNT', 'NBA_FINALS_APPEARANCE', 
                                        'FGM', 'FGA', 'FG_PCT', 'FG3M', 'FG3A', 'FG3_PCT', 'FTM', 'FTA', 'FT_PCT', 'OREB', 'DREB', 'REB', 'AST', 'PF', 'STL', 'TOV', 'BLK', 'PTS', 'PTS_RANK'])

        num = 1
        for i in allteams:
            print(str(num) + "/" + str(30))
            teamID = i["id"]
            teamStats = TeamYearByYearStats(team_id=teamID, league_id='00', season_type_all_star="Regular Season")
            teamStats.get_request()
            teamStats_df = teamStats.get_data_frames()[0]
            main_df = pd.concat([main_df, teamStats_df])
            num+=1
        
        main_df.to_csv("NBATeamStats.csv")
        print("complete")
    
    def getTeamDetails(self, df):
        for i in self.dates:
            teamdets = TeamEstimatedMetrics(season=str(i))
            teamdets.get_request()
            teamdets_df = teamdets.get_data_frames()[0]




