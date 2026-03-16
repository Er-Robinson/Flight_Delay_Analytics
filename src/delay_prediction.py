import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.preprocessing import StandardScaler


class FlightDelayPredictor:

    def __init__(self):

        self.model = GradientBoostingClassifier()
        self.scaler = StandardScaler()

    def train(self, data):

        features = data[[
            "velocity",
            "baro_altitude",
            "vertical_rate"
        ]].fillna(0)

        # Simple delay rule for training label (example)
        data["delay_label"] = (data["vertical_rate"].abs() > 8).astype(int)

        X = self.scaler.fit_transform(features)
        y = data["delay_label"]

        self.model.fit(X, y)

    def predict(self, data):

        features = data[[
            "velocity",
            "baro_altitude",
            "vertical_rate"
        ]].fillna(0)

        X = self.scaler.transform(features)

        predictions = self.model.predict(X)

        data["delay_risk"] = predictions

        return data