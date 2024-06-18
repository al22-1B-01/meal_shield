import os
from pathlib import Path

from dotenv import load_dotenv

PACKAGE_DIR = Path(__file__).parents[2]
load_dotenv(PACKAGE_DIR / '.env')

<<<<<<< HEAD
VERSION = "0.1.0"
=======
VERSION = '0.1.0'
