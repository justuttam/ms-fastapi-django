from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_auth_token: str = None
    debug: bool = False
    echo_active: bool = False
    app_auth_token_prd: str = None

    model_config = SettingsConfigDict(env_file=".env")
