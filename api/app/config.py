from pydantic import BaseSettings
from dotenv import load_dotenv

# env configs:
load_dotenv()

class Settings(BaseSettings):
    db_username: str
    db_password: str
    db_hostname: str
    db_name: str



settings =  Settings()