import tqdm
import pandas as pd

if __name__ == "__main__":
    # df = pd.read_csv("../../../data/temp_data/node_raw.csv")
    # for i in range(len(df)):
    #     df.loc[i]["node"] = df.loc[i]["node"].replace(" ", "")
    # df = df.drop_duplicates(ignore_index=True)
    # df.to_csv("../../../data/node.csv", index=False)
    df = pd.read_csv("../../../data/station_coordinate.csv")
    df = df[["station", "longitude", "latitude"]]
    df.to_csv("../../../data/node_id.csv", index=True)
