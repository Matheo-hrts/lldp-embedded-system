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

def load_history() -> list:
    file_path = "saves/history.csv"
    if not os.path.exists(file_path):
        return []
    with open(file_path, "r") as f:
        reader = csv.DictReader(f)
        return list(reader)

def group_by_system(history: list) -> dict:
    grouped = {}
    for frame in history:
        name = frame["system_name"]
        if name not in grouped:
            grouped[name] = []
        grouped[name].append(frame)
    return grouped
