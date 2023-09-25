import pandas as pd


if __name__ == "__main__":
    node_df = pd.read_csv("../../../data/station_coordinate.csv")
    node_df = node_df[["station", "longitude", "latitude"]]
    node_df = node_df.rename(columns={"station": "Id", "longitude": "lng", "latitude": "lat"})
    node_df.to_csv("../../../data/node_gephi.csv", index=False)
    edge_df = pd.read_csv("../../../data/edge_simple.csv")
    edge_df = edge_df[["start_station_name", "end_station_name", "running_time"]]
    edge_df = edge_df.rename(columns={"start_station_name": "Source", "end_station_name": "Target", "running_time": "Weight"})
    edge_df.to_csv("../../../data/edge_gephi.csv", index=False)
