import requests
import random
import time
import tqdm
import pandas as pd


if __name__ == "__main__":
    character_list = ["C", "D", "G", "K", "S", "T", "Y", "Z"]
    number_list = [str(i) for i in range(10)]
    key_dict = {
        "C": [
            "C1",
            "C20", "C21", "C22", "C23", "C24", "C25", "C26", "C27", "C28", "C29",
            "C3", "C4",
            "C50", "C51", "C52", "C53", "C54", "C55", "C56", "C57", "C58", "C59",
            "C60", "C61", "C62", "C63", "C64", "C65", "C66", "C67", "C68", "C69",
            "C70", "C71", "C72", "C73", "C74", "C75", "C76", "C77", "C78", "C79",
            "C8", "C9"
        ],
        "D": [
            "D10", "D11", "D12", "D13", "D14", "D15", "D16", "D17", "D18", "D19",
            "D20", "D21", "D22", "D23", "D24", "D25", "D26", "D27", "D28", "D29",
            "D30", "D31", "D32", "D33", "D34", "D35", "D36", "D37", "D38", "D39",
            "D4",
            "D50", "D51", "D52", "D53", "D54", "D55", "D56", "D57", "D58", "D59",
            "D60", "D61", "D62", "D63", "D64", "D65", "D66", "D67", "D68", "D69",
            "D70", "D71", "D72", "D73", "D74", "D75", "D76", "D77", "D78", "D79",
            "D80", "D81", "D82", "D83", "D84", "D85", "D86", "D87", "D88", "D89",
            "D90", "D91", "D92", "D93", "D94", "D95", "D96", "D97", "D98", "D99"
        ],
        "G": [
            "G10", "G11", "G12", "G13", "G14", "G15", "G16", "G17", "G18", "G19",
            "G20", "G21", "G22", "G23", "G24", "G25", "G26", "G27", "G28", "G29",
            "G30", "G31", "G32", "G33", "G34", "G35", "G36", "G37", "G38", "G39",
            "G4",
            "G50", "G51", "G52", "G53", "G54", "G55", "G56", "G57", "G58", "G59",
            "G60", "G61", "G62", "G63", "G64", "G65", "G66", "G67", "G68", "G69",
            "G70", "G71", "G72", "G73", "G74", "G75", "G76", "G77", "G78", "G79",
            "G80", "G81", "G82", "G83", "G84", "G85", "G86", "G87", "G88", "G89",
            "G90", "G91", "G92", "G93", "G94", "G95", "G96", "G97", "G98", "G99"
        ],
        "K": [
            "K10", "K11", "K12", "K13", "K14", "K15", "K16", "K17", "K18", "K19",
            "K2", "K3", "K4", "K5", "K6", "K7", "K8", "K9"
        ],
        "S": [
            "S1", "S5", "S6", "S7", "S8", "S9"
        ],
        "T": ["T"],
        "Y": ["Y"],
        "Z": ["Z1", "Z2", "Z3", "Z4", "Z5", "Z6", "Z7", "Z8", "Z9"]
    }

    date_list = ["20230925", "20230926", "20230927", "20230928", "20230929", "20230930",
                 "20231001", "20231002", "20231003", "20231004", "20231005", "20231006",
                 "20231007"]
    station_train_code_dict = {
                                "station_train_code": [],
                                "train_no": []
                               }

    url = "https://search.12306.cn/search/v1/train/search"
    header_list = [
        {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
                          "(KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        },
        {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X -1_0_0) AppleWebKit/537.36 "
                          "(KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"
        },
        {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                          "(KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
        },
        {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                          "(KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.36"
        }
    ]
    params = {"keyword": None, "date": None}
    response = None

    # cnt = 0
    # for key in tqdm.tqdm(key_dict["G"]):
    #     params["keyword"] = key
    #     params["date"] = date_list[random.randint(0, len(date_list) - 1)]
    #
    #     response = requests.get(url=url, headers=header_list[2],
    #                             params=params)
    #     body = response.json()
    #
    #     if "data" in body.keys() and body["data"]:
    #         for i in range(len(body["data"])):
    #             if body["data"][i]["station_train_code"] not in station_train_code_dict["station_train_code"]:
    #                 station_train_code_dict["station_train_code"].append(body["data"][i]["station_train_code"])
    #                 station_train_code_dict["train_no"].append(body["data"][i]["train_no"])
    #     time.sleep(random.uniform(1.2, 3.5))
    #     cnt += 1
    #     if cnt % 5 == 0:
    #         time.sleep(5)
    #
    # df = pd.DataFrame(station_train_code_dict)
    # df.to_csv("../../../data/station_train_code_G.csv", index=False)

    for c in character_list:
        for key in tqdm.tqdm(key_dict[c]):
            params["keyword"] = key
            params["date"] = date_list[random.randint(0, len(date_list) - 1)]

            response = requests.get(url=url, headers=header_list[random.randint(0, len(header_list) - 1)],
                                    params=params)
            body = response.json()

            if "data" in body.keys() and body["data"]:
                for i in range(len(body["data"])):
                    if body["data"][i]["station_train_code"] not in station_train_code_dict["station_train_code"]:
                        station_train_code_dict["station_train_code"].append(body["data"][i]["station_train_code"])
                        station_train_code_dict["train_no"].append(body["data"][i]["train_no"])
            time.sleep(random.uniform(0, 0.5))
        time.sleep(5)

    df = pd.DataFrame(station_train_code_dict)
    df.to_csv("../../../data/station_train_code.csv", index=False)
    # df_list = []
    # for c in tqdm.tqdm(character_list):
    #     df_list.append(pd.read_csv("../../../data/station_train_code_" + c + ".csv"))
    # df = pd.concat(df_list, axis=0, ignore_index=True)
    # df.to_csv("../../../data/station_train_code.csv", index=False)

