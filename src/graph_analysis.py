import pandas as pd
import networkx as nx


class FlightGraphAnalyzer:

    def __init__(self):
        self.graph = nx.DiGraph()

    def build_graph(self, data):

        if "Origin" not in data.columns or "Dest" not in data.columns:
            return self.graph

        for _, row in data.iterrows():

            origin = str(row["Origin"])
            dest = str(row["Dest"])

            if origin != "nan" and dest != "nan":

                # Increase weight if route already exists
                if self.graph.has_edge(origin, dest):
                    self.graph[origin][dest]["weight"] += 1
                else:
                    self.graph.add_edge(origin, dest, weight=1)

        return self.graph

    def busiest_airports(self):

        airport_counts = {}

        for u, v, data in self.graph.edges(data=True):

            weight = data["weight"]

            airport_counts[u] = airport_counts.get(u, 0) + weight
            airport_counts[v] = airport_counts.get(v, 0) + weight

        airport_df = pd.DataFrame(
            airport_counts.items(),
            columns=["Airport", "Flights"]
        )

        airport_df = airport_df.sort_values(
            by="Flights",
            ascending=False
        )

        return airport_df.head(10)