import request as _request
import pandas as pd
import logging as _logging
import json as _json
from dynaconf import Dynaconf
import threading
import sys

""" _logging.basicConfig(
    filename="application.log",
    level=_logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    stream=sys.stdout
) """

file_handler = _logging.FileHandler(filename='application.log')
stdout_handler = _logging.StreamHandler(stream=sys.stdout)
handlers = [file_handler, stdout_handler]

_logging.basicConfig(
    level=_logging.DEBUG, 
    format='[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s',
    handlers=handlers
)

logger = _logging.getLogger('LOGGER_NAME')

headers = {
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0"
}
secrets = Dynaconf(settings_files=["settings.toml", ".secrets.toml"])
alienvault_apikey = secrets.alienvault_apikey


def start_crawl():
    _logging.info("----------- crawl start -----------")
    threads = []
    t = threading.Thread(target=alienvault(), args=())
    t2 = threading.Thread(target=openphish(), args=())
    t3 = threading.Thread(target=phishtank(), args=())

    threads.append(t)
    threads.append(t2)
    threads.append(t3)
    for t in threads:
        if not t.is_alive():
            t.start()

    for t in threads:
        t.join()


def phishtank():
    _logging.info("----------- phishtank start -----------")
    tmp = headers
    tmp["user-agent"] = "phishtank/leofelix"
    r = _request.get_request("http://data.phishtank.com/data/online-valid.csv", tmp)
    if r.status_code != 200:
        _logging.warn("phishtank data crawl stopped : http status not 200")
        return

    f = open("phishtank.csv", "w")
    f.write(r.text)
    f.close()

    try:
        veri = pd.read_csv("phishtank.csv")
        phish_id = veri["phish_id"]
        url = veri["url"]
    except Exception as e:
        _logging.warn("CSV read failed", str(e))

    _logging.info("Phishtank Found : " + str(len(veri)))
    error_counter = 0
    for i in range(len(veri)):
        json = {"resource": "phishtank", "phish_link": url[i]}
        try:
            r = _request.post_request("http://fastapi-service:80/api/phish/", json, headers)
            if r.status_code != 200:
                _logging.warn("phishtank | api http error : http not ok ")
                error_counter += 1
                # if http error >=20 stop
                # phishtank add new urls top of file
                if error_counter >= 20:
                    _logging.warn("phishtank stopped : error counter reached 20 ")

                    break
        except Exception as e:
            _logging.warn("phishtank parse feed and send to api failed ", str(e))


def openphish():
    _logging.info("----------- openphish start -----------")
    try:
        r = _request.get_request("https://openphish.com/feed.txt", headers)
        if r.status_code != 200:
            _logging.warn("openphish stopped : http status not 200")
            return
    except Exception as e:
        _logging.warn("openphish data crawl  failed ", str(e))
    error_counter = 0
    for line in r.text.split("\n"):
        json = {"resource": "openphish", "phish_link": line}
        try:
            r = _request.post_request("http://fastapi-service:80/api/phish/", json, headers)
            if r.status_code != 200:
                _logging.warn("openphish  | api http error : http not ok ")
                error_counter += 1
                if error_counter >= 20:
                    _logging.warn("openphish stopped : error counter reached 20 ")
                    break
        except Exception as e:
            _logging.warn("openphish parse feed and send to api failed ", str(e))


def alienvault():
    _logging.info("----------- alienvault start -----------")
    headers = {"X-OTX-API-KEY": alienvault_apikey}
    # https://otx.alienvault.com/api/v1/pulses/subscribed
    next_page = "https://otx.alienvault.com/otxapi/pulses/63db48cfb1884ba2d5ddf309/indicators/?sort=-created&limit=100&page=1"
    while next_page != None:
        try:
            r = _request.get_request(next_page, headers)
            if r.status_code != 200:
                _logging.warn("alienvault stopped : http status not 200")
                return
        except Exception as e:
            _logging.warn("alienvault get pulse failed ", str(e))

        parsed_data = _json.loads(r.text)

        indicators = parsed_data["results"]
        next_page = parsed_data["next"]
        _logging.info("Crawling alienvault page : " + str(next_page))

        error_counter = 0
        for indicator in indicators:
            indicator_value = indicator["indicator"]
            # print(indicator_value)

            json = {"resource": "alienvault", "phish_link": indicator_value}
            if indicator_value.startswith("http"):
                try:
                    r = _request.post_request(
                        "http://fastapi-service:80/api/phish/", json, None
                    )
                    if r.status_code != 200:
                        _logging.warn("alienvault | api http error : http not ok ")
                        error_counter += 1
                        if error_counter >= 20:
                            _logging.warn(
                                "alienvault stopped : error counter reached 20 "
                            )
                            break
                except Exception as e:
                    _logging.warn("alienvault  send to api failed ", str(e))
