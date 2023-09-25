import requests
import random
import time
import tqdm
import pandas as pd


if __name__ == "__main__":
    station_city_df = pd.read_csv("../../../data/station_city.csv")
    station_coordinate_list = []
    missing_station_coordinate_list = []
    url = "http://api.map.baidu.com/geocoding/v3/"
    params = {
        "address": None,
        "output": "json",
        "ak": "hHuNSIxeWGq9p5h8K9xZRQkkx53qnSk9"
    }
    # params = {
    #     "address": "南阳市内乡火车站",
    #     "output": "json",
    #     "ak": "hHuNSIxeWGq9p5h8K9xZRQkkx53qnSk9"
    # }
    # response = requests.get(url=url, params=params)
    # body = response.json()
    # print(body)
    for i in tqdm.tqdm(range(len(station_city_df))):
        station = station_city_df.loc[i]["station"]
        city = station_city_df.loc[i]["city"]
        params["address"] = city + station + "站"
        response = requests.get(url=url, params=params)
        body = response.json()
        if body["status"] == 0:
            station_coordinate_list.append({
                "station": station,
                "city": city,
                "longitude": body["result"]["location"]["lng"],
                "latitude": body["result"]["location"]["lat"]
            })
        else:
            missing_station_coordinate_list.append({
                "station": station,
                "city": city
            })
        time.sleep(random.uniform(0.03, 0.05))
    df = pd.DataFrame(station_coordinate_list)
    df.to_csv("../../../data/station_coordinate.csv", index=False)
    df = pd.DataFrame(missing_station_coordinate_list)
    df.to_csv("../../../data/missing_station_coordinate.csv", index=False)
    print(missing_station_coordinate_list)
