import CollectData
from sklearn.feature_selection import VarianceThreshold
from sklearn.feature_selection import SelectKBest, f_regression
import numpy as np
import pandas as pd

class FeatureExtractor:
    def __init__(self, df):
        self.df = df
        self.res = df[["key", "NBA_FINALS_APPEARANCE", "CONF_RANK"]]
        self.makeOutput()
        self.cleanData()
        self.extract()

    def extract(self):
        X = self.df
        y = self.res["y"]
        selk = SelectKBest(f_regression, k=20)
        X_new = selk.fit_transform(X, y)
        col = selk.get_feature_names_out()
        new_df = pd.DataFrame(columns=col, data=X_new)
        self.df = new_df

    def makeOutput(self):
        n = self.res.count().key
        self.res["y"] = np.zeros(n)
        for i in range(0, n):
            row = self.res.iloc[i]
            if row["NBA_FINALS_APPEARANCE"] == "LEAGUE CHAMPION":
                self.res.at[i, "y"] = 1
            elif row["NBA_FINALS_APPEARANCE"] == "FINALS APPEARANCE":
                self.res.at[i, "y"] = 2
            else:
                if self.res["CONF_RANK"].iloc[i] <= 8:
                    self.res.at[i, "y"] = 3
                else:
                    continue
    
    def cleanData(self):
        types = self.df.dtypes
        exitCols = ["WINS", "LOSSES", "PO_WINS", "PO_LOSSES", "W", "L", "W_PCT"]
        for i in types.index:
            if types[i] == "object":
                self.df = self.df.drop(columns=i)
            elif i in exitCols:
                self.df = self.df.drop(columns=i)
    
    def printDF(self):
        print(self.df.info())

    def getFeatures(self):
        return self.df, self.res["y"]





    
