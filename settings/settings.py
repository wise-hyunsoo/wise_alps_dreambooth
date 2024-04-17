import os
from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    project_id: str
    project_number: str
    default_location: str
    vertex_bucket: str
    pipeline_registry_host: str
    pipelines_shared_tag: str

    class Config:
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings():
    """Create an instance of the Settings class
        that returns the appropriate settings value for each environment from the dotenv file and environment variables.

    Notice:
        - If you don't change the default Config (case_sensitive = False), it is case-insensitive.
            ex.> PROJECT_ID and project_id are recognized as the same.
        - The dotenv variable that is not declared as a Settings class field is ignored.

    Priority:
        1. System environment variables
        2. The dotenv variables
            The higher the index, the higher the priority.
            When _env_file=(".env", f".env.prod"), .env.prod has a higher priority.
        3. Settings class default field value
    """

    # save current working directory
    cwd = os.getcwd()

    # change working directory to the directory of this file
    abspath = os.path.abspath(__file__)
    os.chdir(os.path.dirname(abspath))

    env = os.getenv("ENVIRONMENT", "local")
    settings = Settings(_env_file=(".env", f".env.{env}"))
    print(f"settings for {env} environment:{settings.dict()}")

    # change working directory back to the original
    os.chdir(cwd)

    return settings
