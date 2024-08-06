import os
from dotenv import load_dotenv
class ENV:
  load_dotenv()
  PORT= int(os.getenv("PORT", 8082))
  MONGO_URI = os.getenv("MONGO_URI", "")
  API_KEY = os.getenv("API_KEY", "")
  DATABASE_NAME = os.getenv("DATABASE_NAME", "")
  COLLECTION_NAME = os.getenv("COLLECTION_NAME", "")
  MODEL = os.getenv("MODEL", "")