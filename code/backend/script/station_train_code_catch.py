import requests
import random
import time
import tqdm
import pandas as pd


character_list = [chr(i) for i in range(ord("A"), ord("Z") + 1)]
date_list = ["20230925", "20230926", "20230927", "20230928", "20230929", "20230930",
             "20231001", "20231002", "20231003", "20231004", "20231005", "20231006"]
station_train_code_dict = {"station_train_code": [],
                           "train_no": []}

url = "https://search.12306.cn/search/v1/train/search"
headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
                          "(KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
           }
params = {"keyword": None, "date": None}
response = None

for c in tqdm.tqdm(character_list):
    params["keyword"] = c
    params["date"] = date_list[random.randint(0, len(date_list) - 1)]
    response = requests.get(url=url, headers=headers, params=params)
    body = response.json()
    if "data" in body.keys() and body["data"]:
        for i in range(len(body["data"])):
            station_train_code_dict["station_train_code"].append(body["data"][i]["station_train_code"])
            station_train_code_dict["train_no"].append(body["data"][i]["train_no"])
    time.sleep(random.randint(0, 3))

df = pd.DataFrame(station_train_code_dict)
df.to_csv("../../../data/station_train_code.csv", index=False)
