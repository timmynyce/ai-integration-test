import json
import os
from datetime import datetime


def write_log(log_folder: str, log_record: dict) -> str:
    os.makedirs(log_folder, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    path = os.path.join(log_folder, f"log_{timestamp}.json")

    with open(path, "w", encoding="utf-8") as f:
        json.dump(log_record, f, indent=2)

    return path