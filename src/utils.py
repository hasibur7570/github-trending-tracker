import os
import yaml
from datetime import datetime

def load_config(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)
    
def ensure_folder_exists(folder_path: str):
    os.makedirs(folder_path, exist_ok=True)

def get_today_date() -> str:
    return datetime.now().strftime("%Y-%m-%d")



