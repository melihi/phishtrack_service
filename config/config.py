from dynaconf import Dynaconf
import logging
import sys

settings = Dynaconf(
    envvar_prefix="DYNACONF",
    settings_files=["../settings.toml", "../.secrets.toml"],
)


def setup_logger(logger_name, logfile):
    """
    Create logger .

    Args :
        logger_name (str) : logger name .
        logfile (str) : log file name .

    """
    file_handler = logging.FileHandler(filename="./data/" + logfile)
    stdout_handler = logging.StreamHandler(stream=sys.stdout)
    handlers = [file_handler, stdout_handler]

    logging.basicConfig(
        level=logging.DEBUG,
        format="[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s",
        handlers=handlers,
    )

    logger = logging.getLogger(logger_name)
    return logger
