"""The project settings like the database connection URL."""

from environs import Env

env = Env()
env.read_env()


class Settings:
    # Project settings.
    PROJECT_NAME = "WaniKani parser"
    PATH_TO_PROJECT = "/home/jakefish/Documents/GitHub/wanikani-parser/src"

    # Database settings.
    database_url = env("DATABASE_URL")

    # Parser settings.
    request_headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"
    }
    WANIKANI_BASE_URL = "https://www.wanikani.com"


settings = Settings()
