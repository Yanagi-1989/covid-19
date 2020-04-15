import json

import pandas as pd
import requests

# 東京都_新型コロナ受診相談窓口相談件数 CSVファイル
TEL_CSV_URL = "https://stopcovid19.metro.tokyo.lg.jp/data/130001_tokyo_covid19_combined_telephone_advice_center.csv"
# 東京都_新型コロナウイルス陽性患者発表詳細
PATIENTS_CSV_URL = "https://stopcovid19.metro.tokyo.lg.jp/data/130001_tokyo_covid19_patients.csv"

# 東京都 新型コロナウイルス感染症対策サイト オープンデータ Json
DATA_JSON_URL = "https://raw.githubusercontent.com/tokyo-metropolitan-gov/covid19/development/data/data.json"

# CSVをデータフレーム化
res = requests.get(TEL_CSV_URL)
csv_data = [row.split(",") for row in res.content.decode("utf-8-sig").split("\r\n")]
tel_csv_df = pd.DataFrame(csv_data[1:], columns=csv_data[0])

# 東京都 新型コロナウイルス感染症対策サイトにて公開されている情報を取得
res = requests.get(DATA_JSON_URL)
data_json = json.loads(res.content.decode())

# 検査実施人数
inspection_persons = json.loads(res.content.decode())["inspection_persons"]
label = inspection_persons["labels"]
data = inspection_persons["datasets"][0]["data"]
dataset_df = pd.DataFrame(zip([date_str[:10] for date_str in label], data), columns=["検査日", "検査実施人数"])

# 陽性者数
patients_df = pd.DataFrame([(dict_["日付"][:10], dict_["小計"]) for dict_ in data_json["patients_summary"]["data"]],
                           columns=["日付", "小計"])

# 検査日 == 陽性が判明した日付(?)としてデータフレームを結合
joined_df = pd.merge(dataset_df, patients_df, left_on=["検査日"], right_on=["日付"])
# 陽性数/検査数 を計算
joined_df["陽性数/検査数"] = joined_df["小計"] / joined_df["検査実施人数"]

# 計算結果をCSV出力
joined_df.to_csv("result.csv", encoding="sjis")
