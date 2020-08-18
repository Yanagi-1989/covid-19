import os

from sqlalchemy import asc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy import Column, TIMESTAMP, DATE, CHAR, Integer

from datetime import datetime

# 以下の条件を満たすため、利用ユーザ数が増えない限りDBはsqlite3で良いと思ってる
#   - テーブル更新はcronでの定期実行のみ
#   - ユーザ情報等は特に保持しない
engine = create_engine(f"sqlite:///{os.environ['DB_PATH']}", echo=True)

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
    def fetch_num(cls, prefecture_code):
        """指定した都道府県の日毎の感染者数を取得.

        クエリは以下と同等.

        SELECT
          publication_date,
          num
        FROM
          patient
        WHERE
          prefecture_code = $prefecture_code
        ORDER BY
          publication_date ASC

        Parameters
        ----------
        prefecture_code: str
            2桁の都道府県コード

        Returns
        -------
        list[PatientsModel]"""
        # sqlite3ではセッションの永続化を行えないため、逐一セッションを作成する。
        db_session = DBSession()

        records = db_session.query(cls.publication_date, cls.num) \
            .filter(cls.prefecture_code == prefecture_code) \
            .order_by(asc(cls.publication_date)) \
            .all()

        db_session.close()

        return records
