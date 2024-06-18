import os
from pathlib import Path

from dotenv import load_dotenv

PACKAGE_DIR = Path(__file__).parents[2]
load_dotenv(PACKAGE_DIR / '.env')

VERSION = '0.1.0'

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
