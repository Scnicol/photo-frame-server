#allows for managing different environments (development, testing, production).
import os
class Config:
    DB_PATH = os.getenv("DB_PATH", "sqlite:///instance/photos.db")
