import os
from datetime import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy import Column, TIMESTAMP, DATE, CHAR, Integer

from csv_file import NHKPrefecturesCSV

# 以下の条件を満たすため、利用ユーザ数が増えない限りDBはsqlite3で良いと思ってる
#   - テーブル更新はcronでの定期実行のみ
#   - ユーザ情報等は特に保持しない
db_file_path = f"{os.path.dirname(os.path.dirname(os.path.abspath(__file__)))}/sqlite3.db"

engine = create_engine(f"sqlite:///{db_file_path}", echo=True)

# テーブル用クラス作成するとき継承
Base = declarative_base()
# DBとのセッションクラス
DBSession = sessionmaker(bind=engine)


class PatientsModel(Base):
    """感染者数テーブル"""

    __tablename__ = "patient"

    # 都道府県コード(JISX0401)
    prefecture_code = Column(CHAR(2), primary_key=True)
    # 発症または感染が公表された年月日
    publication_date = Column(DATE, primary_key=True)
    # 感染者数
    num = Column(Integer)
    # 作成日時
    created_at = Column(TIMESTAMP, default=datetime.now)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.publication_date}, num:{self.num})"

    @classmethod
    def gen_models(cls, df):
        """データフレームからモデルを作成.

        Parameters
        ----------
        df: pandas.DataFrame
            感染者情報のデータフレーム

        Returns
        -------
        list[PatientsModel]"""
        models = []

        for idx in range(len(df)):
            # 情報を生成
            publication_date = datetime.strptime(df.iloc[idx][NHKPrefecturesCSV.CSV_DATE_COL_NAME], "%Y/%m/%d")
            num = df.iloc[idx][NHKPrefecturesCSV.CSV_NUM_NAME]
            prefecture_code = df.iloc[idx][NHKPrefecturesCSV.CSV_PREFECTURE_CODE_NAME]
            # 1レコード分の情報生成
            table = PatientsModel()
            table.publication_date = publication_date
            table.num = num
            table.prefecture_code = prefecture_code

            models.append(table)

        return models

    @classmethod
    def delete_insert(cls, models):
        """テーブルをDELETE/INSERT

        Parameters
        ----------
        models: list[PatientsModel]
            INSERT対象のDBモデルリスト"""
        db_session = DBSession(autocommit=True)
        db_session.begin()

        try:
            db_session.query(PatientsModel).delete()
            db_session.add_all(models)
        except Exception:
            db_session.rollback()
            raise
        else:
            db_session.commit()


def init_db():
    # テーブルがDBにない場合テーブルを作成
    Base.metadata.create_all(engine)
