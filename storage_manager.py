import csv
import os
from datetime import datetime

def save_csv(data: dict) -> None:
    data = data.copy()
    data["timestamp"] = datetime.now()
    fieldnames = data.keys()
    dir_path = "saves"
    dir_exists = os.path.exists(dir_path)
    if not dir_exists:
        os.mkdir(dir_path)
    file_path = "saves/history.csv"
    file_exists = os.path.exists(file_path)
    with open(file_path, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow(data)
