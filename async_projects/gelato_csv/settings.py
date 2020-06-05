from dotenv import load_dotenv
import os
from pathlib import Path

env_path = Path('.')
load_dotenv(dotenv_path=env_path)

GELATO_KEY = os.getenv("GELATO_API_URL_KEY")