import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler


class FlightPatternDiscovery:

    def __init__(self, clusters=3):

        self.k = clusters
        self.scaler = StandardScaler()
        self.model = KMeans(n_clusters=self.k, random_state=42)

    def discover(self, data):

        features = data[[
            "velocity",
            "baro_altitude",
            "vertical_rate"
        ]].fillna(0)

        scaled = self.scaler.fit_transform(features)

        data["cluster"] = self.model.fit_predict(scaled)

        return data

class PatternDiscovery:

    def altitude_velocity_pattern(self, df):

        print("\nDiscovering altitude vs velocity pattern...")

        plt.figure(figsize=(8,6))
        sns.scatterplot(
            x=df["baro_altitude"],
            y=df["velocity"],
            alpha=0.5
        )

        plt.title("Altitude vs Velocity Pattern")
        plt.xlabel("Altitude")
        plt.ylabel("Velocity")
        plt.show()


    def airline_distribution(self, df):

        print("\nAirline traffic distribution...")

        airline_counts = df["Airline"].value_counts().head(10)

        airline_counts.plot(kind="bar")

        plt.title("Top Airlines Traffic")
        plt.ylabel("Number of Flights")
        plt.show()


    def geo_density(self, df):

        print("\nFlight location density...")

        plt.figure(figsize=(8,6))

        sns.kdeplot(
            x=df["longitude"],
            y=df["latitude"],
            fill=True
        )

        plt.title("Flight Density Map")
        plt.show()

import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler


class FlightPatternDiscovery:

    def __init__(self, clusters=3):

        self.k = clusters
        self.scaler = StandardScaler()
        self.model = KMeans(n_clusters=self.k, random_state=42)

    def discover(self, data):

        features = data[[
            "velocity",
            "baro_altitude",
            "vertical_rate"
        ]].fillna(0)

        scaled = self.scaler.fit_transform(features)

        data["cluster"] = self.model.fit_predict(scaled)

        return data