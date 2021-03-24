import pandas as pd
import requests


class NHKNationwideCSV:
    # 全国の1日毎の感染者数(NHKまとめ)
    URL = "https://www3.nhk.or.jp/n-data/opendata/coronavirus/nhk_news_covid19_domestic_daily_data.csv"

    # ファイルのエンコーディング等の情報
    FILE_ENCODING = "utf-8-sig"
    FILE_NEWLINE = "\r\n"
    # CSV/TSVファイルの区切り文字
    FILE_SPLIT = ","

    # CSVファイルの各列の情報
    CSV_DATE_COL_NAME = "日付"
    CSV_NUM_NAME = "国内の感染者数_1日ごとの発表数"

    # 列とそのデータ型
    CSV_COLUMN_D_TYPES = {
        CSV_DATE_COL_NAME: str,
        CSV_NUM_NAME: int
    }

    # 日本全国を指す都道府県コード(あくまで便宜上)
    NATIONWIDE_PREFECTURE_CODE = "00"

    @classmethod
    def _fetch(cls):
        """公開されている感染者情報のCSVを取得する.

        Returns
        -------
        str"""
        res = requests.get(cls.URL)
        if res.status_code != 200:
            raise Exception("NHKが配布しているCSVファイル取得失敗")

        return res.content.decode(cls.FILE_ENCODING)

    @classmethod
    def _format_patients_df(cls, content):
        """感染者数情報CSVの文字列から、感染者数のDataFrameを作成.

        Parameters
        ----------
        content: str

        Returns
        -------
        pandas.DataFrame"""
        # CSV情報からDataFrameを生成
        csv_data = [row.split(cls.FILE_SPLIT) for row in content.split(cls.FILE_NEWLINE)[:-1]]
        patients_df = pd.DataFrame(csv_data[1:], columns=csv_data[0])

        # 必要な列のデータ型を修正
        ret = patients_df.astype(cls.CSV_COLUMN_D_TYPES)

        return ret

    @classmethod
    def gen_df(cls):
        """公開されているファイルから、感染者数のDataFrameを作成.

        Returns
        -------
        pandas.DataFrame"""
        prefecture_df = cls._format_patients_df(cls._fetch())
        # 都道府県毎の情報から、不必要な列情報を削除
        prefecture_df = prefecture_df[cls.CSV_COLUMN_D_TYPES.keys()]

        return prefecture_df


class NHKPrefecturesCSV:
    # ファイルが存在するURL
    # 都道府県ごとの感染者数（累計・NHKまとめ）
    # https://www3.nhk.or.jp/news/special/coronavirus/data/
    URL = "https://www3.nhk.or.jp/n-data/opendata/coronavirus/nhk_news_covid19_prefectures_daily_data.csv"

    # ファイルのエンコーディング等の情報
    FILE_ENCODING = "utf-8-sig"
    FILE_NEWLINE = "\r\n"
    # CSV/TSVファイルの区切り文字
    FILE_SPLIT = ","

    # CSVファイルの各列の情報
    CSV_DATE_COL_NAME = "日付"
    CSV_PREFECTURE_CODE_NAME = "都道府県コード"
    CSV_NUM_NAME = "各地の感染者数_1日ごとの発表数"

    # 列とそのデータ型
    CSV_COLUMN_D_TYPES = {
        CSV_DATE_COL_NAME: str,
        CSV_PREFECTURE_CODE_NAME: str,
        CSV_NUM_NAME: int
    }

    @classmethod
    def _fetch(cls):
        """公開されている感染者情報のCSVを取得する.

        Returns
        -------
        str"""
        res = requests.get(cls.URL)
        if res.status_code != 200:
            raise Exception("NHKが配布しているCSVファイル取得失敗")

        return res.content.decode(cls.FILE_ENCODING)

    @classmethod
    def _format_patients_df(cls, content):
        """感染者数情報CSVの文字列から、感染者数のDataFrameを作成.

        Parameters
        ----------
        content: str

        Returns
        -------
        pandas.DataFrame"""
        # CSV情報からDataFrameを生成
        csv_data = [row.split(cls.FILE_SPLIT) for row in content.split(cls.FILE_NEWLINE)[:-1]]
        patients_df = pd.DataFrame(csv_data[1:], columns=csv_data[0])

        # 必要な列のデータ型を修正
        ret = patients_df.astype(cls.CSV_COLUMN_D_TYPES)

        return ret

    @classmethod
    def gen_df(cls):
        """公開されているファイルから、感染者数のDataFrameを作成.

        Returns
        -------
        pandas.DataFrame"""
        prefecture_df = cls._format_patients_df(cls._fetch())
        # 都道府県毎の情報から、不必要な列情報を削除
        prefecture_df = prefecture_df[cls.CSV_COLUMN_D_TYPES.keys()]

        return prefecture_df
