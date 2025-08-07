from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Database configuration
    database_url: str = Field(

        description="PostgreSQL database connection URL"
    )

    # JWT configuration
    jwt_secret_key: str = Field(

        description="Secret key for JWT token signing"
    )
    jwt_algorithm: str = Field(

        description="JWT signing algorithm"
    )
    jwt_access_token_expire_minutes: int = Field(

        description="JWT token expiration time in minutes"
    )

    # Server configuration
    host: str = Field(

        description="Server host"
    )
    port: int = Field(

        description="Server port"
    )
    debug: bool = Field(

        description="Debug mode"
    )

    # Database logging configuration
    database_logging: bool = Field(
        default=False,
        description="Enable database query logging"
    )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


settings = Settings()
