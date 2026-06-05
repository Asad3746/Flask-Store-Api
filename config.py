import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "mysql+pymysql://root:@localhost/my_store",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    LOG_DIR = os.environ.get("LOG_DIR", "logs")
    LOG_FILE = os.environ.get("LOG_FILE", "app.log")

    @classmethod
    def validate(cls):
        if not cls.SQLALCHEMY_DATABASE_URI:
            raise ValueError(
                "DATABASE_URL is not set. Copy .env.example to .env and add your database URL."
            )
