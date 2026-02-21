import requests
import os
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv

#Cargo las credenciales
load_dotenv()
SERVER_USER = os.getenv("USER_SERVER")
SERVER_PASSWORD = os.getenv("PASSWORD_SERVER")

#Hora local
utc_minus_5 = timezone(timedelta(hours=-5))


#Traigo los logs de AGH vía HTTP
response = requests.get(
    "http://192.168.1.16/control/querylog",
    auth=(SERVER_USER, SERVER_PASSWORD)   
)


response.raise_for_status()
data = response.json()["data"]
print(f"Total registros recibidos: {len(data)}")
#print(data[0]['time'])


if not data:
    print("No hay datos.")
    exit()

# Extraer los timestamps
timestamps = []

for item in data:
    ts = item['time'].replace("Z", "+00:00")
    utc_time = datetime.fromisoformat(ts)
    local_time = utc_time.astimezone(utc_minus_5)
    timestamps.append(local_time)

min_time = min(timestamps)
max_time = max(timestamps)


print(f'primero: {data[0]["time"]}') 
print(f'ultimo: {data[-1]["time"]}')

print(f"Registro más antiguo: {min_time}")
print(f"Registro más reciente: {max_time}")
#print(f"Rango cubierto: {max_time - min_time}")