import os
import pathlib
from google.oauth2.service_account import Credentials

from dotenv import load_dotenv

load_dotenv()
TOPIC_NAME = "messages"

if os.environ.get("LOCAL"):
    SERVICE_ACCOUNT_SECRET_PATH = os.path.join(
        pathlib.Path(__file__).parent, "gemini-insights-sa-key.json"
    )
    sa_credentials_for_clients = Credentials.from_service_account_file(
        SERVICE_ACCOUNT_SECRET_PATH
    )
