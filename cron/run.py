if __name__ == '__main__':
    from csv_file import NHKPrefecturesCSV
    from db import init_db, PatientsModel

    init_db()
    # NHKが配布しているCSVからDataFrameを生成
    df = NHKPrefecturesCSV.gen_df()
    # DataFrameをDBテーブルモデルに変換
    models = PatientsModel.gen_models(df)
    # DBに情報をDELETE/INSERT
    PatientsModel.delete_insert(models)
