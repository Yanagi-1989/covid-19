if __name__ == '__main__':
    from csv_file import CSVTokyo
    from db import init_db, PatientsModel

    init_db()

    df = CSVTokyo().format_patients_df()

    models = PatientsModel.gen_models(df, CSVTokyo.prefecture_code, CSVTokyo.num_col_name)
    PatientsModel.delete_insert(models)
