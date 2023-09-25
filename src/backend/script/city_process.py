import tqdm
import pandas as pd


if __name__ == "__main__":
    station_df = pd.read_csv("../../../data/node.csv")
    station_list = station_df.to_dict(orient='list')['node']
    station_city_df = pd.read_csv("../../../data/station_city_raw.csv")
    del_rows = []
    for i in range(len(station_city_df)):
        if station_city_df.loc[i]["station"] not in station_list:
            del_rows.append(i)
    station_city_df = station_city_df.drop(labels=del_rows)
    station_city_df.to_csv("../../../data/station_city.csv", index=False)
