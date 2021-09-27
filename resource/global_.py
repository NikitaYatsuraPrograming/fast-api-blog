from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from pydantic import BaseSettings


class Settings(BaseSettings):
    secret_key: str = "Awesome API"
    algorithm: str
    access_token_expire_minutes: int
    database_login: str
    database_password: str
    database_host: str
    database_port: int
    database_name: str

    class Config:
        env_file = ".env"


settings = Settings()

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

DATABASE_LOGIN = settings.database_login
DATABASE_PASSWORD = settings.database_password
DATABASE_HOST = settings.database_host
DATABASE_PORT = settings.database_port
DATABASE_NAME = settings.database_name

SQLALCHEMY_DATABASE_URL = \
    f"postgresql+asyncpg://{DATABASE_LOGIN}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"
SQLALCHEMY_DATABASE_URL_NO_ASYNC = \
    f"postgresql+asyncpg://{DATABASE_LOGIN}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")
