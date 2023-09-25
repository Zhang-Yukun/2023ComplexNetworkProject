import requests
import random
import time
import tqdm
import pandas as pd


def time_minus(start_time, end_time):
    start_hour, start_minute = map(int, start_time.split(":"))
    end_hour, end_minute = map(int, end_time.split(":"))
    if end_hour < start_hour:
        end_hour += 24
    if end_minute - start_minute > 0:
        result_minute = end_minute - start_minute
    else:
        result_minute = end_minute - start_minute + 60
        end_hour -= 1
    result_hour = end_hour - start_hour
    result = result_hour * 60 + result_minute
    return result


if __name__ == "__main__":
    df = pd.read_csv("../../../data/temp_data/station_train_code.csv")
    station_train_code_dict = df.to_dict(orient="index")

    date_list = ["2023-09-25", "2023-09-26", "2023-09-27", "2023-09-28", "2023-09-29", "2023-09-30",
                 "2023-10-01", "2023-10-02", "2023-10-03", "2023-10-04", "2023-10-05", "2023-10-06"]
    station_train_code_list = []
    node_list = []
    edge_list = []

    url = "https://kyfw.12306.cn/otn/queryTrainInfo/query"
    headers = {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
                              "(KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
               }
    params = {"leftTicketDTO.train_no": None,
              "leftTicketDTO.train_date": None,
              "rand_code": ""}
    response = None
    for i in tqdm.tqdm(range(len(station_train_code_dict))):
        params["leftTicketDTO.train_no"] = station_train_code_dict[i]["train_no"]
        params["leftTicketDTO.train_date"] = date_list[random.randint(0, len(date_list) - 1)]
        response = requests.get(url=url, headers=headers, params=params)
        body = response.json()
        if "data" in body.keys() and body["data"] and "data" in body["data"].keys() and body["data"]["data"]:
            if body["data"]["data"][0]["station_name"] not in node_list:
                node_list.append(body["data"]["data"][0]["station_name"])
            for j in range(1, len(body["data"]["data"])):
                if body["data"]["data"][j]["station_name"] not in node_list:
                    node_list.append(body["data"]["data"][j]["station_name"])
                start_station_name = body["data"]["data"][j - 1]["station_name"]
                end_station_name = body["data"]["data"][j]["station_name"]
                station_train_code = station_train_code_dict[i]["station_train_code"]
                running_time = time_minus(body["data"]["data"][j - 1]["start_time"], body["data"]["data"][j]["arrive_time"])
                edge_list.append({
                                "start_station_name": start_station_name,
                                "end_station_name": end_station_name,
                                "running_time": running_time,
                                "train_no": station_train_code
                                })
        # time.sleep(random.randint(0, 2))
    # print(node_list)
    # print(edge_list)
    df = pd.DataFrame(node_list, columns=["node"])
    df.to_csv("../../../data/node_raw.csv", index=False)
    df = pd.DataFrame(edge_list)
    df.to_csv("../../../data/edge_multiply.csv", index=False)
