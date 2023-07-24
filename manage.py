import click
import uvicorn
 
from crawler.main_crawler import main_crawler

from config.config import setup_logger

LOGGER = setup_logger("phishtrack", "phish_tracker.log")

@click.command()
@click.option("--api", "-a", is_flag=True, help="Run api service")
@click.option("--crawler", "-c", is_flag=True, help="Run crawler service")
def manage(api, crawler):
    """Phish track manage cli"""
    if api:
        uvicorn.run("phish_track.api.api:app", host="0.0.0.0", port=8000, reload=True)

    elif crawler:
        main_crawler()


# won't run when imported , if executed as script manage function will start
if __name__ == "__main__":
    manage()
