from os import environ as env

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Standards format
DATE_FORMAT_RESULT = env.get("DATE_FORTMAT_RESULT", "%d-%b-%Y")

# Flask
TEMPLATES_PATH = env.get("TEMPLATES_PATH", "templates")
SECRET_KEY = env.get("SECRET_KEY")
HOSTNAME = env.get("HOSTNAME", "0.0.0.0")
PORT = int(env.get("PORT", "5000"))
DEBUG_MODE = bool(env.get("DEBUG", "False"))
