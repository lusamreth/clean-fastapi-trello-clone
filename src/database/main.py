from sqlalchemy.orm import (
    declarative_base,
    sessionmaker,
    DeclarativeBase,
)
from sqlalchemy import MetaData, create_engine, text

database = "jrello"
url = "mysql+mysqldb://lusomreth:Somreth012618653@127.0.0.1:3306/{}".format(
    database
)

Base = declarative_base()


class Database:
    def __init__(self, url=url):
        self.engine = create_engine(url, echo=True)
        self.autoCreateDB()
        self.initializeDB()

    def autoCreateDB(self):
        with self.engine.connect() as conn:
            conn.execute(
                text(f"CREATE DATABASE IF NOT EXISTS {database}")
            )
            conn.execute(text(f"USE {database}"))

    def initializeDB(self):
        Base.metadata.create_all(bind=self.engine, checkfirst=True)

    def getSession(self):
        Session = sessionmaker(self.engine)
        return Session
