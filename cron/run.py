if __name__ == '__main__':
    from csv_file import CSVBase
    from db import init_db, PatientsModel

    init_db()

    for cls in CSVBase.__subclasses__():
        df = cls().format_patients_df()

        models = PatientsModel.gen_models(df, cls.prefecture_code, cls.num_col_name)
        PatientsModel.delete_insert(models, cls.prefecture_code)
