import os
from dotenv import load_dotenv
from pathlib import Path

env_path = Path('.') / '.env'  # Path to .env file
load_dotenv(dotenv_path=env_path)  # Load .env file

class Settings:
    POSTGRES_USER: str = os.getenv('POSTGRES_USER')
    POSTGRES_PASSWORD: str = os.getenv('POSTGRES_PASSWORD')
    POSTGRES_DB: str = os.getenv('POSTGRES_DB')
    POSTGRES_HOST: str = os.getenv('POSTGRES_HOST')
    POSTGRES_PORT: int = os.getenv('POSTGRES_PORT')
    SQLALCHEMY_DATABASE_URI: str = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    SECRET_KEY = os.getenv('SECRET_KEY')
    ALGORITHM = os.getenv('ALGORITHM')
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))
    PROJECT_NAME = os.getenv('PROJECT_NAME')

    def __str__(self):
        return (
            f'PROJECT_NAME: {self.PROJECT_NAME}\n'
            f'POSTGRES_USER: {self.POSTGRES_USER}\n'
            f'POSTGRES_PASSWORD: {self.POSTGRES_PASSWORD}\n'
            f'POSTGRES_DB: {self.POSTGRES_DB}\n'
            f'POSTGRES_HOST: {self.POSTGRES_HOST}\n'
            f'POSTGRES_PORT: {self.POSTGRES_PORT}\n'
            f'SQLALCHEMY_DATABASE_URI: {self.SQLALCHEMY_DATABASE_URI}\n'
            f'SQLALCHEMY_TRACK_MODIFICATIONS: {self.SQLALCHEMY_TRACK_MODIFICATIONS}\n'
            f'SECRET_KEY: {self.SECRET_KEY}\n'
            f'ALGORITHM: {self.ALGORITHM}\n'
            f'ACCESS_TOKEN_EXPIRE_MINUTES: {self.ACCESS_TOKEN_EXPIRE_MINUTES}'
        )

settings = Settings() # Create an instance of the Settings class
