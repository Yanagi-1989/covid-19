import pandas as pd
import requests


class CSVBase:
    """感染者数のCSV"""

    # 都道府県コード(JISX0401)
    prefecture_code = None
    # CSVファイルが公開されているURL
    url = None
    # ローカル保存時のファイル名
    file_name = "local.csv"
    # 公表された年月日の列名
    date_col_name = "公表_年月日"
    # 感染者数の列名(独自に命名)
    num_col_name = "人数"
    # CSVのエンコード
    csv_encoding = "utf-8-sig"

    def __init__(self):
        # TODO: CSVの列目チェック
        # TODO: エンコードチェック
        self.patients_df = self._fetch()

    def _fetch(self):
        """公開されている感染者情報のCSVを取得する.

        Returns
        -------
        pandas.DataFrame"""
        res = requests.get(self.url)
        csv_data = [row.split(",") for row in res.content.decode(self.csv_encoding).split("\r\n")[:-1]]
        patients_df = pd.DataFrame(csv_data[1:], columns=csv_data[0])

        return patients_df

    def save_file(self):
        self.patients_df.to_csv(self.file_name)

    def format_patients_df(self):
        """感染者数のDataFrameを整形.

        1. 列は日付と感染者数のみ
        2. 感染者数が1人もいない日は0人とカウント(日付を飛ばさない)

        Returns
        -------
        pandas.DataFrame"""
        # 日付列のみを抽出
        patients_df = self.patients_df[[self.date_col_name]]
        # 日付毎の感染者数を算出するための列を追加
        patients_df[self.num_col_name] = 1
        # 0人埋めしたデータフレームを生成
        zero_df = self._gen_zero_df()
        # データフレームを連結
        patients_df = pd.concat([zero_df, patients_df]).reset_index(drop=True)
        # 日付毎に陽性者数を集計
        grouped_df = patients_df.groupby([self.date_col_name]).sum()

        return grouped_df

    def _gen_zero_df(self):
        """範囲内の全ての日付に対し、0人のデータフレームを作成.

        Returns
        -------
        pandas.DataFrame"""
        dates = pd.date_range(start=min(self.patients_df[self.date_col_name]),
                              end=max(self.patients_df[self.date_col_name]))
        dates_df = pd.DataFrame([(_date.strftime("%Y-%m-%d"), 0) for _date in dates],
                                columns=[self.date_col_name, self.num_col_name])
        return dates_df


class CSVHokkaido(CSVBase):
    prefecture_code = "01"
    url = "https://www.harp.lg.jp/opendata/dataset/1369/resource/3132/010006_hokkaido_covid19_patients.csv"
    csv_encoding = "sjis"


class CSVTokyo(CSVBase):
    prefecture_code = "13"
    url = "https://stopcovid19.metro.tokyo.lg.jp/data/130001_tokyo_covid19_patients.csv"
