import tqdm
import pandas as pd


if __name__ == "__main__":
    df = pd.read_csv("../../../data/temp_data/edge_multiply_raw.csv")
    for i in tqdm.tqdm(range(len(df))):
        df.loc[i, ["start_station_name"]] = df.loc[i]["start_station_name"].replace(" ", "")
        df.loc[i, ["end_station_name"]] = df.loc[i]["end_station_name"].replace(" ", "")
    df.to_csv("../../../data/temp_data/edge_multiply.csv", index=False)
    df = pd.read_csv("../../../data/temp_data/edge_multiply.csv")
    edge_set = set()
    edge_list = []
    df = df.sort_values(by="running_time")
    for index, row in df.iterrows():
        if (((row["start_station_name"], row["end_station_name"]) not in edge_set)
                and ((row["end_station_name"], row["start_station_name"]) not in edge_set)):
            edge_list.append({
                "start_station_name": row["start_station_name"],
                "end_station_name": row["end_station_name"],
                "running_time": row["running_time"],
                "train_no": row["train_no"]
            })
            edge_set.add((row["start_station_name"], row["end_station_name"]))
    df = pd.DataFrame(edge_list)
    df.to_csv("../../../data/edge_simple.csv", index=False)

