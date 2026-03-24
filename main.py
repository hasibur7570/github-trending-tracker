import sys
import os
import pprint

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from src.database import DatabaseManager
from src.utils import load_config, ensure_folder_exists, get_today_date
from src.scraper import GitHubScraper
from src.stats import summarize_stats


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
        scraper = GitHubScraper(url, headers=headers)
        try:
            repos = scraper.scrape_trending()
            db.insert_repos(today, repos)
            print(f"Inserted/Updated: {len(repos)} repos for {today}")
        except Exception as e:
            print(f"Exception occured while scraping data from github. Error: {e}")
    try:
        # user can see github_trending_repos of Daily, Weekly, or Monthly
        # taking input from user as -> 1 == daily, -1 == last 7 days, -2 == Monthly
        days = int(input("Enter number of days to analyze (e.g. 7): ").strip())
    except Exception:
        print("Invalid input! Defaulting to last 7 days")
        days = 7
    
    rows = db.fetch_last_n_days(days)
    if not rows:
        print("No data found! Exiting.")
        return
    else:
        stats = summarize_stats(rows, top_n=cfg["plot"]["top_n"], min_presence_pct=0.3)
    print("\n========== Stats ===========")
    pprint.pprint(stats) 



if __name__ == "__main__":
    main()