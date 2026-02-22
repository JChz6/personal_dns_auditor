import json
from datetime import datetime
from pathlib import Path



def save_batch_locally(records : list):
    if not records:
        print('No hay records')
        return

    now = datetime.utcnow()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H-%M-%S")

    base_path = Path("/home/cheesus/proyectos/dns_auditor/personal_dns_auditor/files") / date_str
    base_path.mkdir(parents=True, exist_ok=True)

    file_path = base_path / f"batch_{date_str}T{time_str}.json"

    with open(file_path, "w") as f:
        for record in records:
            f.write(json.dumps(record) + "\n")

    print(f"Batch guardado en {file_path}")