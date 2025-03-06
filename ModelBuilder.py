import CollectData
import FeatureExtractor
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
# import tensorflow as tf
# from keras.utils import FeatureSpace
# import keras.models
# import keras.layers
# from tensorflow.keras.optimizers.legacy import Adam

class ModelBuilder:

    def __init__(self):
        self.DE = CollectData.dataExtractor().getDataframe()
        self.FE = FeatureExtractor.FeatureExtractor(self.DE)
        self.df = self.FE.getDf()
        self.t_model = None
        self.y = self.df['y']
        self.X = self.df.drop(columns='y')

        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.X, self.y, test_size=0.33, random_state=42)

        self.BuildModel(self.df)
    
    def BuildModel(self, fs):
        self.t_model = RandomForestClassifier(n_estimators=500, max_depth=2, random_state=0)
    
    def getSummary(self):
        self.t_model.summary()

    def train(self):
        self.t_model.fit(self.X_train, self.y_train)
    
    def eval(self):
        return self.t_model.score(self.X_test, self.y_test)
        

m = ModelBuilder()
m.train()
print(m.eval())

        



    

