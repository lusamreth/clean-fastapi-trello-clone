from sqlalchemy.orm import (
    declarative_base,
    sessionmaker,
    DeclarativeBase,
)
from sqlalchemy import MetaData, create_engine, text
from configs.settings import getSettings

database = "jrello"


def databaseFormat(host, port, username, password, dialect):
    # 127.0.0.1
    db_url = f"{dialect}://{username}:{password}@{host}:{port}"
    return db_url


dbSettings = getSettings()
DATABASE_URL = databaseFormat(
    host=dbSettings.DATABASE_HOSTNAME,
    password=dbSettings.DATABASE_PASSWORD,
    port=dbSettings.DATABASE_PORT,
    username=dbSettings.DATABASE_USERNAME,
    dialect=dbSettings.DATABASE_DIALECT,
)

Base = declarative_base()


class Database:
    def __init__(self, url=DATABASE_URL):
        self.engine = create_engine(url, echo=True, isolation_level="AUTOCOMMIT")
        self.engine_url = url
        self.autoCreateDB()
        self.initializeDB()

    def autoCreateDB(self):
        with self.engine.connect() as conn:
            conn.execute(text("commit"))
            conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {database}"))
            conn.execute(text(f"USE {database}"))
            self.engine_url = "{}/{}".format(self.engine_url, database)
            self.engine = create_engine(self.engine_url)

    def initializeDB(self):
        Base.metadata.create_all(bind=self.engine, checkfirst=True)

    def getSession(self):
        Session = sessionmaker(self.engine)
        return Session
