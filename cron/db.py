import os

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy import Column, TIMESTAMP, DATE, CHAR, Integer

from datetime import datetime

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
        return f"{self.__class__.__name__}({self.publication_date}:{self.num})"

    @classmethod
    def gen_models(cls, df, prefecture_code, num_col_name):
        """データフレームからモデルを作成.

        Parameters
        ----------
        df: pandas.DataFrame
        prefecture_code: str
            都道府県コード
        num_col_name: str

        Returns
        -------
        list[PatientsModel]"""
        models = []
        for idx in range(len(df)):
            table = PatientsModel()
            table.publication_date = datetime.strptime(df.iloc[idx].name, "%Y-%m-%d")
            table.num = int(df.iloc[idx][num_col_name])
            table.prefecture_code = prefecture_code

            models.append(table)

        return models

    @classmethod
    def delete_insert(cls, models):
        """テーブルをDELETE/INSERT

        Parameters
        ----------
        models: list[PatientsModel]"""
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
