import pandas as pd
import requests


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
    def _add_nationwide(cls, prefecture_df):
        """都道府県コード'00'の、全国の感染者数がわかるレコードを追加する.

        Parameters
        ----------
        prefecture_df: pandas.DataFrame
            47都道府県の情報が格納されたデータフレーム

        Returns
        -------
        pandas.DataFrame
            47都道府県に加え、日本全国のその日毎の感染者数情報が格納されたデータフレーム"""
        # 全国の感染者情報を保持したDataFrameを生成
        nationwide_df = prefecture_df.groupby([cls.CSV_DATE_COL_NAME]).sum().reset_index(drop=False)
        nationwide_df[cls.CSV_PREFECTURE_CODE_NAME] = cls.NATIONWIDE_PREFECTURE_CODE  # 便宜上のコード'00'
        nationwide_df = nationwide_df.reindex(columns=cls.CSV_COLUMN_D_TYPES.keys())  # 列の順番を並び替え

        # 都道府県毎の情報に、全国の情報を追加
        ret = pd.concat([prefecture_df, nationwide_df]).reset_index(drop=True)

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

        return cls._add_nationwide(prefecture_df)
