from pydantic import BaseSettings, AnyUrl

class Settings(BaseSettings):
    # dbusername: str 
    # dbpassword: str
    # dbname: str
    # dbcontainername: str
    # dbport: str

    # class Config:
    #     env_file = ".env"

    BOOKS_PROVIDER_URL: AnyUrl = "https://openlibrary.org/api/books?bibkeys=ISBN:{isbn}&format=json&jscmd=details"
    # DATABASE_URL = "postgresql://{dbusername}:{dbpassword}@{dbcontainername}:{dbport}/{dbname}"
    DATABASE_URL = "sqlite:///./books-manager.db"
    DB_LIST_LIMIT = 50

settings = Settings()