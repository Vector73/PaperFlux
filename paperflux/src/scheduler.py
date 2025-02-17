import time
import asyncio
from apscheduler.schedulers.background import BackgroundScheduler
from tasks import run_paper_fetch_job
from datetime import datetime


def job():
    print("Fetching papers 📝")
    asyncio.run(run_paper_fetch_job())


def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(job, "interval", hours=24, next_run_time=datetime.now())
    scheduler.start()
    print("Scheduler started. Running in background.")

    try:
        while True:
            time.sleep(60)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        print("Scheduler stopped.")
