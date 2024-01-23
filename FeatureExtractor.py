import CollectData
from sklearn.feature_selection import VarianceThreshold
from sklearn.feature_selection import SelectKBest, f_regression
import numpy as np
import pandas as pd
import tensorflow as tf
from keras.utils import FeatureSpace

class FeatureExtractor:
    def __init__(self, df):
        self.df = df
        self.res = df[["key", "NBA_FINALS_APPEARANCE", "CONF_RANK"]]
        self.makeOutput()
        self.cleanData()
        self.extract()


        val_dataframe = self.df.sample(frac=0.2, random_state=1337)
        train_dataframe = self.df.drop(val_dataframe.index)
        self.val_ds = self.readyForTF(val_dataframe)
        self.train_ds = self.readyForTF(train_dataframe)
        self.train_ds = self.train_ds.batch(32)
        self.val_ds = self.val_ds.batch(32)
        self.featurespace = self.makeFeatureSpace()

    def extract(self):
        X = self.df
        y = self.res["y"]
        selk = SelectKBest(f_regression, k=20)
        X_new = selk.fit_transform(X, y)
        col = selk.get_feature_names_out()
        new_df = pd.DataFrame(columns=col, data=X_new)
        print(new_df.dtypes)
        new_df["y"] = y
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
        exitCols = ["WINS", "LOSSES", "PO_WINS", "PO_LOSSES", "W", "L", "W_PCT","CONF_RANK", "DIV_RANK", "W_RANK", "L_RANK"]
        for i in types.index:
            if types[i] == "object":
                self.df = self.df.drop(columns=i)
            elif i in exitCols:
                self.df = self.df.drop(columns=i)
    
    def printDF(self):
        print(self.df.info())

    def readyForTF(self, data):
        df = data.copy()
        labels = df.pop("y")
        ds = tf.data.Dataset.from_tensor_slices((dict(df), labels))
        ds = ds.shuffle(buffer_size=len(df))
        return ds

    def getDatasets(self):
        return self.train_ds, self.val_ds

    def getFeatureSpace(self):
        return self.featurespace
    
    def makeFeatureSpace(self):
        features = {
            "WIN_PCT":"float_normalized",
            "FG_PCT":"float_normalized",
            "FG3_PCT":"float_normalized",
            "DREB":"float_normalized",
            "TOV": "float_normalized",
            "PTS_RANK":"float_normalized",
            "E_OFF_RATING":"float_normalized",
            "E_DEF_RATING":         "float_normalized",
            "E_NET_RATING":         "float_normalized",
            "E_AST_RATIO":          "float_normalized",
            "E_REB_PCT":            "float_normalized",
            "E_TM_TOV_PCT":         "float_normalized",
            "W_PCT_RANK":           "float_normalized",
            "E_OFF_RATING_RANK":    "float_normalized",
            "E_DEF_RATING_RANK":    "float_normalized",
            "E_NET_RATING_RANK":    "float_normalized",
            "E_AST_RATIO_RANK":     "float_normalized",
            "E_DREB_PCT_RANK":      "float_normalized",
            "E_REB_PCT_RANK":       "float_normalized",
            "E_TM_TOV_PCT_RANK":    "float_normalized"
        }
        feature_space = FeatureSpace(features=features, output_mode="concat")
        return feature_space





    
