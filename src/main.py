from extract_agh_logs import run_extraction
from transform_logs import transform_logs
from persist_logs import save_batch_locally 
#from load import load_to_bq

logs = run_extraction()

if logs:
    transformed = transform_logs(logs)
    #print(transformed)
    save_batch_locally(transformed)

    #load_to_bq(transformed)
