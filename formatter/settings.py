import os

from pydantic_settings import BaseSettings


class EncryptionSettings(BaseSettings):
    RECEIVE_KEY: str
    RECEIVE_IV: str
    SEND_KEY: str
    SEND_IV: str
    AUTH_TOKEN: str


settings = EncryptionSettings(_env_file=os.environ.get('ENV_FILE', '.env.local'))
