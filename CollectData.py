import csv
import pandas as pd
import math
from nba_api.stats.endpoints import TeamYearByYearStats
from nba_api.stats.endpoints import TeamEstimatedMetrics
from nba_api.stats.static import teams

class dataExtractor:
    # dates = [2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 
    #             2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022]
    def __init__(self):
        self.dates = []
        self.main_df = pd.DataFrame()

    def getHistoricalData(self):
        #Getting main dataframe
        print("Starting")
        allteams = teams.get_teams()
        main_df = pd.DataFrame(columns=['TEAM_ID', 'TEAM_CITY', 'TEAM_NAME', 'YEAR', 'GP', 'WINS', 'LOSSES', 'WIN_PCT', 'CONF_RANK', 'DIV_RANK', 'PO_WINS', 'PO_LOSSES', 'CONF_COUNT', 'DIV_COUNT', 'NBA_FINALS_APPEARANCE', 
                                        'FGM', 'FGA', 'FG_PCT', 'FG3M', 'FG3A', 'FG3_PCT', 'FTM', 'FTA', 'FT_PCT', 'OREB', 'DREB', 'REB', 'AST', 'PF', 'STL', 'TOV', 'BLK', 'PTS', 'PTS_RANK'])

        for i in allteams:
            teamID = i["id"]
            teamStats = TeamYearByYearStats(team_id=teamID, league_id='00', season_type_all_star="Regular Season")
            teamStats.get_request()
            teamStats_df = teamStats.get_data_frames()[0]
            main_df = pd.concat([main_df, teamStats_df])

        #Filtering by dates
        self.setDates(main_df)
        filter1 = main_df["YEAR"].isin(self.dates)
        main_df[filter1]

        print("Getting team details")
        teamdeats_df = self.getTeamDetails()

        print("Joining")
        main_df["key"] = main_df["YEAR"] + main_df["TEAM_ID"].astype('str')
        teamdeats_df["key"] = teamdeats_df["YEAR"] + teamdeats_df["TEAM_ID"]
        main_df.set_index('key').join(teamdeats_df.set_index('key'), how='inner')
        self.main_df = main_df

        

    
    def getTeamDetails(self):
        teamdets_Main = pd.DataFrame(columns=['TEAM_NAME', 'TEAM_ID', 'GP', 'W', 'L', 'W_PCT', 'MIN', 'E_OFF_RATING', 'E_DEF_RATING', 'E_NET_RATING', 'E_PACE', 'E_AST_RATIO', 'E_OREB_PCT', 'E_DREB_PCT', 
                                              'E_REB_PCT', 'E_TM_TOV_PCT', 'GP_RANK', 'W_RANK', 'L_RANK', 'W_PCT_RANK', 'MIN_RANK', 'E_OFF_RATING_RANK', 'E_DEF_RATING_RANK', 'E_NET_RATING_RANK', 'E_AST_RATIO_RANK', 'E_OREB_PCT_RANK', 'E_DREB_PCT_RANK', 'E_REB_PCT_RANK', 'E_TM_TOV_PCT_RANK', 'E_PACE_RANK'])
        for i in self.dates:
            teamdets = TeamEstimatedMetrics(season=str(i))
            teamdets.get_request()
            teamdets_df = teamdets.get_data_frames()[0]
            teamdets_df['YEAR'] = [i for x in range(len(teamdets_df['TEAM_NAME']))]
            teamdets_Main = pd.concat([teamdets_Main, teamdets_df])
        
        return teamdets_Main
    
    def setDates(self, df):
        dates = list(pd.unique(df['YEAR']))
        self.dates = dates[len(dates)-21:]
    
    def printDF(self):
        print(self.main_df.head())
    
    def getDataframe(self):
        return self.main_df


DE = dataExtractor()
DE.getHistoricalData()
DE.printDF()







