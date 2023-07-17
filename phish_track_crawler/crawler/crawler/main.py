import crawl as _crawl
from apscheduler.schedulers.blocking import BlockingScheduler
 

 

def main():
    scheduler = BlockingScheduler(daemon=True)
    scheduler.add_job(_crawl.start_crawl, "interval", minutes=2, max_instances=1)
     
    scheduler.start()


main()
