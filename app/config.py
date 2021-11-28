from pydantic import BaseSettings


# this makes the app requiring the environment variables specified. if i dont specify a default and the env variable is not set it will through am error
class Settings(BaseSettings):
    # these are env variables case insensitive
    database_hostname: str
    database_port: str
    database_name: str
    database_username: str
    database_password: str
    secrete_key: str
    algorithm: str
    access_token_expire_minute: int

    class Config:
        env_file = ".env"


settings = Settings()
