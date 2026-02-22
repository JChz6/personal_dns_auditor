import requests
import os
import json
from pathlib import Path
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv

#Cargo las credenciales
load_dotenv()
BASE_URL = "http://192.168.1.16/control/querylog"
SERVER_USER = os.getenv("USER_SERVER")
SERVER_PASSWORD = os.getenv("PASSWORD_SERVER")

BASE_DIR = Path(__file__).resolve().parent
STATE_FILE = BASE_DIR / "state.json"

utc_minus_5 = timezone(timedelta(hours=-5))

#Trae el último timestamp de la última ejecución
def load_state():
    if not os.path.exists(STATE_FILE):
        return None
    
    with open(STATE_FILE, 'r') as f:
        return json.load(f).get('last_timestamp')


#Guarda el timestamp de la ejecución presente
def save_state(timestamp):
    with open(STATE_FILE, 'w') as f:
        json.dump({'last_timestamp': timestamp}, f)

#Convertir fecha a timestamp
from datetime import datetime, timezone

def iso_to_unix(ts):
    dt = datetime.strptime(ts[:26], "%Y-%m-%dT%H:%M:%S.%f")
    dt = dt.replace(tzinfo=timezone.utc)
    return int(dt.timestamp())



#Traer los logs de AGH
def fetch_logs(last_timestamp=None):
    params = {'limit': 1000}

    response = requests.get(
        BASE_URL,
        params=params,
        auth=(SERVER_USER, SERVER_PASSWORD)
    )

    response.raise_for_status()
    data = response.json()["data"]

    if not last_timestamp:
        return data

    filtered = [
        log for log in data
        if log["time"] > last_timestamp
    ]

    return filtered


#Orquestar
def run_extraction():
    last_timestamp = load_state()
    raw_logs = fetch_logs(last_timestamp)

    if raw_logs:
        newest_timestamp = raw_logs[0]['time']
        save_state(newest_timestamp)

    return raw_logs