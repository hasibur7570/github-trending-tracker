import sys
import os
import pprint

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from src.database import DatabaseManager
from src.utils import load_config, ensure_folder_exists, get_today_date


def main():
    cfg = load_config(os.path.join(PROJECT_ROOT, "config", "config.yaml"))

    data_folder = os.path.join(PROJECT_ROOT, "data")
    output_folder = os.path.join(PROJECT_ROOT, cfg["output"]["folder"])
    db_path = os.path.join(PROJECT_ROOT, cfg["database"]["path"])

    ensure_folder_exists(data_folder)
    ensure_folder_exists(output_folder)

    db = DatabaseManager(db_path)
    today = get_today_date()

    if db.date_exists(today):
        print(f"Data for today already exists! Skipping scrape and insert for date: {today}")
    else:
        url = cfg["scraper"]["trending_url"]
        if cfg["scraper"].get("since"):
            sep = "&" if "?" in url else "?"
            url = f"{url}{sep}since={cfg['scraper']['since']}"
        headers={"user-agent": cfg["scraper"].get("user_agent", "Mozilla/5.0")}

        print("Starting scrape: ", url)


if __name__ == "__main__":
    main()