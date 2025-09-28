import logging
logging.basicConfig(
    filename='data/raw/ingestion.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s'
)

def log_upload(filename, status, info=""):
    logging.info(f"UPLOAD: {filename} STATUS: {status} INFO: {info}")
def log_error(filename, err):
    logging.error(f"ERROR: {filename} DETAIL: {err}")
