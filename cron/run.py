if __name__ == '__main__':
    from csv_file import NHKPrefecturesCSV, NHKNationwideCSV
    from db import init_db, PatientsModel

    init_db()
    # NHKが配布しているCSVからDataFrameを生成
    prefectures_df = NHKPrefecturesCSV.gen_df()
    nationwide_df = NHKNationwideCSV.gen_df()
    # DataFrameをDBテーブルモデルに変換
    models = PatientsModel.gen_models(prefectures_df, nationwide_df)
    # DBに情報をDELETE/INSERT
    PatientsModel.delete_insert(models)
