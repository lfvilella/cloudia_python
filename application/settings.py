from environs import Env
from dotenv import load_dotenv
from dotenv import find_dotenv


env = Env()
load_dotenv(find_dotenv())


FB_VERIFY_TOKEN = env("FB_VERIFY_TOKEN", None)
FB_ACCESS_TOKEN = env("FB_ACCESS_TOKEN", None)
TELEGRAM_TOKEN = env("TELEGRAM_TOKEN", None)
TELEGRAM_URL = env("TELEGRAM_URL", None)
