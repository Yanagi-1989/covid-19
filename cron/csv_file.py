import pandas as pd
import requests
from datetime import datetime, timedelta


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


# TODO: 一応動作するが、URL等がこれからどう動くかわからないため、これを使用する場合は単純なcron使用をやめ、都道府県バッチ等に切り替える必要がある.
# class CSVAomori(CSVBase):
#     prefecture_code = "02"
#     # ファイルURLが不定
#     url = ""
#     # ファイルURLのテンプレート date_strに日付文字列が入る
#     url_base = "https://opendata.pref.aomori.lg.jp/dataset/1531/resource/11827/02_{date_str}_%E9%99%BD%E6%80%A7%E6%82%A3%E8%80%85%E9%96%A2%E4%BF%82.csv" # NOQA
#     csv_encoding = "sjis"
#
#     def __init__(self):
#         self._set_url()
#         super().__init__()
#
#     def _set_url(self):
#         """直近のCSVファイルURLをセットする.
#
#         青森県のCSVファイルURLは固定ではなく以下のようになっている模様.
#         https://{domain}/dataset/1531/resource/11827/02_YYYYMMDD
#
#         YYYYMMDDの部分がどのタイミングで更新されるかわからないため、
#         直近100日間で総当りし、存在する中で一番新しい日付のCSVを使用する."""
#         from datetime import datetime, timedelta
#
#         num = 0
#         today = datetime.now()
#         while num < 100:
#             date_ = today - timedelta(days=num)
#             date_str = date_.strftime("%Y%m%d")
#             url = self.url_base.format(date_str=date_str)
#             res = requests.get(url)
#
#             # ファイルが存在した場合はそのURLを使用する
#             if res.status_code == 200:
#                 self.url = url
#                 break
#             num += 1
#
#     def format_patients_df(self):
#         """日付の文字列がYYYY-MM-DDの形式では無いため修正する必要がある."""
#
#         temp_df = self.patients_df[self.date_col_name]
#
#         def format_date(date_):
#             """日付文字列フォーマットを修正(YY日MM月DD日→YY-MM-DD)"""
#             return datetime.strptime(date_, "%Y年%m月%d日").strftime("%Y-%m-%d")
#
#         formatted_dates = [format_date(date_) for date_ in temp_df]
#
#         self.patients_df[self.date_col_name] = formatted_dates
#         return super().format_patients_df()


class CSVTokyo(CSVBase):
    prefecture_code = "13"
    url = "https://stopcovid19.metro.tokyo.lg.jp/data/130001_tokyo_covid19_patients.csv"


class CSVFukui(CSVBase):
    prefecture_code = "18"
    url = "https://www.pref.fukui.lg.jp/doc/toukei-jouhou/covid-19_d/fil/covid19_patients.csv"
    # 公表された年月日のフォーマット
    date_col_fmt = "%Y/%m/%d"

    def format_date(self):
        """日付文字列を修正"""
        dates = self.patients_df[self.date_col_name]

        def func(date_):
            return datetime.strptime(date_, self.date_col_fmt).strftime("%Y-%m-%d")

        formatted_dates = [func(date_) for date_ in dates]
        return formatted_dates

    def format_patients_df(self):
        self.patients_df[self.date_col_name] = self.format_date()
        return super().format_patients_df()


class CSVGifu(CSVBase):
    prefecture_code = "21"
    url = "https://data.gifu-opendata.pref.gifu.lg.jp/dataset/4661bf9d-6f75-43fb-9d59-f02eb84bb6e3/resource/9c35ee55-a140-4cd8-a266-a74edf60aa80/download/210005gifucovid19patients.csv" # NOQA
    csv_encoding = "sjis"


class CSVShizuoka(CSVBase):
    prefecture_code = "22"
    url = "https://opendata.pref.shizuoka.jp/dataset/8167/resource/46279/220001_shizuoka_covid19_patients.csv"
    csv_encoding = "sjis"
    # 公表された年月日のフォーマット
    date_col_fmt = "%Y/%m/%d"

    def format_date(self):
        """日付文字列を修正"""
        dates = self.patients_df[self.date_col_name]

        def func(date_):
            return datetime.strptime(date_, self.date_col_fmt).strftime("%Y-%m-%d")

        formatted_dates = [func(date_) for date_ in dates]
        return formatted_dates

    def format_patients_df(self):
        self.patients_df[self.date_col_name] = self.format_date()
        return super().format_patients_df()


class CSVYamaguchi(CSVBase):
    prefecture_code = "35"
    url = "https://yamaguchi-opendata.jp/ckan/dataset/f6e5cff9-ae43-4cd9-a398-085187277edf/resource/f56e6552-4c5d-4ec6-91c0-090f553e0aea/download/350001_yamaguchi_covid19_patients.csv" # NOQA
    date_col_name = "公表日"

    # 公表された年月日のフォーマット
    date_col_fmt = "%Y/%m/%d"

    def format_date(self):
        """日付文字列を修正"""
        dates = self.patients_df[self.date_col_name]

        def func(date_):
            return datetime.strptime(date_, self.date_col_fmt).strftime("%Y-%m-%d")

        formatted_dates = [func(date_) for date_ in dates]
        return formatted_dates

    def format_patients_df(self):
        self.patients_df[self.date_col_name] = self.format_date()
        return super().format_patients_df()
