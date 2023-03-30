from pydantic import BaseSettings
import os



class DBSettings(BaseSettings):
    username: str
    password: str
    database: str
    host: str
    port: str

    class Config:
        env_prefix = "DB_"
        env_file = os.path.expanduser(".env")
