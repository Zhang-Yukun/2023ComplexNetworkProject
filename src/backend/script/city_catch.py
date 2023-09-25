import requests
import re
import random
import time
import tqdm
import pandas as pd


if __name__ == "__main__":
    station_city_list = []
    missing_station_list = []
    url = "https://www.12306.cn/index/script/core/common/station_name_new_v10016.js"
    headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
                          "(KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    }
    response = requests.get(url=url, headers=headers)
    body = response.text
    data = ((((body[body.index("'") + 1:body.rindex("'")]
            .replace("@wxi|万象|YTM|wanxiang|wx|21|9206|万象|lao|老挝|vientiane", ""))
            .replace("@mdi|磨丁|VBM|moding|md|876|9203|磨丁|lao|老挝|Boten", ""))
            .replace("@lbb|琅勃拉邦|VJM|langbolabang|lblb|2258|9207|琅勃拉邦|lao|老挝|Luang Prabang", ""))
            .replace("@wro|万荣|VOM|wanrong|wr|2890|9202|老挝万荣|lao|老挝|Vang Vieng", ""))
    data = re.split(r'@|\||\|\|\|', data)
    while '' in data:
        data.remove('')
    for i in range(1317):
        station_city_list.append({"station": data[i * 8 + 1], "city": data[i * 8 + 7]})
    for i in range(1317, len(data) // 8):
        station_city_list.append({"station": data[i * 8 + 2], "city": data[i * 8 + 8]})
    # for station in tqdm.tqdm(station_list):
    #     if station not in data:
    #         missing_station_list.append(station)
    # print(missing_station_list)

    df = pd.DataFrame(station_city_list)
    df.to_csv("../../../data/station_city_raw.csv", index=False)
