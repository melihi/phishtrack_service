from apscheduler.schedulers.blocking import BlockingScheduler


from .crawl_engine.crawl import *

DEFAULT_TIME = 10


def main_crawler():
    """
    Add jobs to apscheduler .
    """
    scheduler = BlockingScheduler(
        daemon=True,
    )
    scheduler.add_job(
        crawl_phishtank, "interval", seconds=DEFAULT_TIME, max_instances=1
    )
    scheduler.add_job(
        crawl_openphish, "interval", seconds=DEFAULT_TIME, max_instances=1
    )
    scheduler.add_job(
        crawl_alienvault, "interval", seconds=DEFAULT_TIME, max_instances=1
    )
    scheduler.add_job(
        crawl_phishing_database_github,
        "interval",
        seconds=DEFAULT_TIME,
        max_instances=1,
    )
    scheduler.add_job(
        crawl_phishing_army, "interval", seconds=DEFAULT_TIME, max_instances=1
    )
    scheduler.add_job(
        crawl_tweet_feed, "interval", seconds=DEFAULT_TIME, max_instances=1
    )
    scheduler.add_job(crawl_usom, "interval", seconds=DEFAULT_TIME, max_instances=1)
    scheduler.add_job(crawl_certpl, "interval", minutes=5, max_instances=1)
    scheduler.add_job(
        crawl_some_saglikgov, "interval", seconds=DEFAULT_TIME, max_instances=1
    )
    scheduler.add_job(
        crawl_phishhunt, "interval", seconds=DEFAULT_TIME, max_instances=1
    )
    scheduler.start()
