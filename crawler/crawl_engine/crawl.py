import json
import logging

import pandas as pd

from config.config import *

from ..database.database import bulk_insert_users
from ..http.request import *


HEADERS = {
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0"
}


ALIENVAULT_APIKEY = settings.alienvault_apikey
PHISHING_ARMY = "https://phishing.army/download/phishing_army_blocklist_extended.txt"
PHISHTANK = "http://data.phishtank.com/data/online-valid.csv"
OPENPHISH = "https://openphish.com/feed.txt"
PHISHHUNT = "https://phishunt.io/feed.txt"
ALIENVAULT = "https://otx.alienvault.com/otxapi/pulses/63db48cfb1884ba2d5ddf309/indicators/?sort=-created&limit=100&page=1"
PHISHING_DATABASE_GITHUB = "https://raw.githubusercontent.com/mitchellkrogza/Phishing.Database/master/phishing-links-NEW-today.txt"
TWEET_FEED = "https://api.tweetfeed.live/v1/today/phishing/url"
SOME_SAGLIKGOV = (
    "https://dosyamerkez.saglik.gov.tr/Eklenti/43243/0/zararli-url-listesi.txt"
)
CERTPL = "https://hole.cert.pl/domains/domains.txt"


def crawl_phishtank():
    """Crawl source : http://data.phishtank.com/data/online-valid.csv
    Response data format : csv
    Update Rate : Unknown
    """

    logging.info("----------- phishtank start -----------")
    tmp = HEADERS
    tmp["user-agent"] = "phishtank/leofelix"
    r = get_request(PHISHTANK, tmp)
    if r.status_code != 200:
        logging.warn("phishtank data crawl stopped : http status not 200")
        return

    f = open("phishtank.csv", "w")
    f.write(r.text)
    f.close()
    users_data = []
    try:
        veri = pd.read_csv("phishtank.csv")

        url = veri["url"]
    except Exception as e:
        logging.warn("CSV read failed", str(e))

    logging.info("Phishtank Found : " + str(len(veri)))

    try:
        for i in range(len(veri)):
            data = {"resource": "phishtank", "phish_link": url[i]}

            users_data.append(data)
            if len(users_data) % 10000 == 0:
                bulk_insert_users(users_data)
                users_data = []

        # if data count under 10k insert anyway
        bulk_insert_users(users_data)
    except Exception as e:
        logging.warn("phishtank parse feed and send to api failed ", str(e))


def crawl_openphish():
    """Crawl source : https://openphish.com/feed.txt
    Response data format : txt
    Update Rate : Unknown
    """
    logging.info("----------- openphish start -----------")
    try:
        r = get_request(OPENPHISH, HEADERS)
        if r.status_code != 200:
            logging.warn("openphish stopped : http status not 200")
            return
    except Exception as e:
        logging.warn("openphish data crawl  failed ", str(e))
    users_data = []

    lines = r.text.split("\n")
    logging.info("openphish Found : " + str(len(lines)))
    try:
        for line in lines:
            data = {"resource": "openphish", "phish_link": line}
            users_data.append(data)
            if len(users_data) % 10000 == 0:
                bulk_insert_users(users_data)
                users_data = []

        # if data count under 10k insert anyway
        bulk_insert_users(users_data)
    except Exception as e:
        logging.warn("openphish parse feed and send to api failed ", str(e))


def crawl_alienvault():
    """Crawl source : https://otx.alienvault.com/otxapi/pulses/63db48cfb1884ba2d5ddf309/indicators/?sort=-created&limit=100&page=1
    Response data format : json
    Update Rate : Unknown
    """

    logging.info("----------- alienvault start -----------")
    headers = {"X-OTX-API-KEY": ALIENVAULT_APIKEY}

    next_page = ALIENVAULT
    users_data = []
    while next_page != None:
        try:
            r = get_request(next_page, headers)
            if r.status_code != 200:
                logging.warn("alienvault stopped : http status not 200")
                return
        except Exception as e:
            logging.warn("alienvault get pulse failed ", str(e))

        parsed_data = json.loads(r.text)

        indicators = parsed_data["results"]
        next_page = parsed_data["next"]
        logging.info("Crawling alienvault page : " + str(next_page))
        logging.info("Crawling alienvault found : " + str(len(indicators)))

        try:
            for indicator in indicators:
                indicator_value = indicator["indicator"]
                data = {"resource": "alienvault", "phish_link": indicator_value}
                if indicator_value.startswith("http"):
                    users_data.append(data)
                    if len(users_data) % 10000 == 0:
                        bulk_insert_users(users_data)
                        users_data = []

            # if data count under 10k insert anyway
            bulk_insert_users(users_data)
        except Exception as e:
            logging.warn("alienvault  send to api failed ", str(e))


def crawl_phishing_database_github():
    """Crawl source : https://raw.githubusercontent.com/mitchellkrogza/Phishing.Database/master/phishing-links-NEW-today.txt
    Response data format : txt
    Update Rate : Daily
    """

    logging.info("----------- phishing_database_github start -----------")
    try:
        r = get_request(
            PHISHING_DATABASE_GITHUB,
            HEADERS,
        )
        if r.status_code != 200:
            logging.warn("phishing_database_github stopped : http status not 200")
            return
    except Exception as e:
        logging.warn("phishing_database_github data crawl  failed ", str(e))
    users_data = []
    lines = r.text.split("\n")
    logging.info("Crawling phishing_database_github found : " + str(len(lines)))
    try:
        for line in lines:
            data = {"resource": "phishing_database_github", "phish_link": line}
            users_data.append(data)
            if len(users_data) % 10000 == 0:
                bulk_insert_users(users_data)
                users_data = []

        # if data count under 10k insert anyway
        bulk_insert_users(users_data)
    except Exception as e:
        logging.warn(
            "phishing_database_github parse feed and send to api failed ", str(e)
        )


def crawl_phishing_army():
    """Crawl source : https://phishing.army/download/phishing_army_blocklist_extended.txt
    Response data format : txt
    Update Rate : 6 hours
    """

    logging.info("----------- phishing_army start -----------")

    try:
        r = get_request(
            PHISHING_ARMY,
            HEADERS,
        )
        if r.status_code != 200:
            logging.warn("phishing_army stopped : http status not 200")
            return
    except Exception as e:
        logging.warn("phishing_army data crawl  failed ", str(e))
    users_data = []
    lines = r.text.split("\n")
    logging.info("Crawling phishing_army found : " + str(len(lines)))
    try:
        for line in lines:
            if not line.startswith("#"):
                data = {"resource": "phishing_army", "phish_link": line}
                users_data.append(data)
                if len(users_data) % 10000 == 0:
                    bulk_insert_users(users_data)
                    users_data = []

        # if data count under 10k insert anyway
        bulk_insert_users(users_data)
    except Exception as e:
        logging.warn("phishing_army parse feed and send to api failed ", str(e))


def crawl_tweet_feed():
    """Crawl source : https://api.tweetfeed.live/v1/today/phishing/url
    Response data format : json
    Update Rate : Daily
    """
    logging.info("----------- tweet_feed start -----------")

    users_data = []

    try:
        r = get_request(TWEET_FEED, HEADERS)
        if r.status_code != 200:
            logging.warn("tweet_feed stopped : http status not 200")
            return
    except Exception as e:
        logging.warn("tweet_feed get pulse failed ", str(e))

    parsed_data = json.loads(r.text)
    logging.info("Crawling tweet_feed found : " + str(len(parsed_data)))
    try:
        for value in parsed_data:
            data = {"resource": "tweet_feed", "phish_link": value["value"]}

            users_data.append(data)
            if len(users_data) % 10000 == 0:
                bulk_insert_users(users_data)
                users_data = []
        # if data count under 10k insert anyway
        bulk_insert_users(users_data)
    except Exception as e:
        logging.warn("tweet_feed  send to api failed ", str(e))


def crawl_usom():
    """Crawl source : https://www.usom.gov.tr/url-list.txt
    Response data format : txt
    Update Rate : 5 min
    """
    logging.info("----------- usom start -----------")

    try:
        r = get_request(
            "https://www.usom.gov.tr/url-list.txt",
            HEADERS,
        )
        if r.status_code != 200:
            logging.warn("usom stopped : http status not 200")
            return
    except Exception as e:
        logging.warn("usom data crawl  failed ", str(e))
    users_data = []
    lines = r.text.split("\n")
    logging.info("Crawling usom found : " + str(len(lines)))
    try:
        for line in lines:
            data = {"resource": "usom", "phish_link": line}
            users_data.append(data)
            if len(users_data) % 10000 == 0:
                bulk_insert_users(users_data)
                users_data = []

        # if data count under 10k insert anyway
        bulk_insert_users(users_data)
    except Exception as e:
        logging.warn("usom parse feed and send to api failed ", str(e))


def crawl_certpl():
    """Crawl source : https://hole.cert.pl/domains/domains.txt
    Response data format : txt
    Update Rate : 5 min
    """
    logging.info("----------- certpl start -----------")

    try:
        r = get_request(
            CERTPL,
            HEADERS,
        )
        if r.status_code != 200:
            logging.warn("certpl stopped : http status not 200")
            return
    except Exception as e:
        logging.warn("certpl data crawl  failed ", str(e))
    users_data = []
    lines = r.text.split("\n")
    logging.info("Crawling certpl found : " + str(len(lines)))
    try:
        for line in lines:
            data = {"resource": "certpl", "phish_link": line}
            users_data.append(data)
            if len(users_data) % 10000 == 0:
                bulk_insert_users(users_data)
                users_data = []

        # if data count under 10k insert anyway
        bulk_insert_users(users_data)
    except Exception as e:
        logging.warn("certpl parse feed and send to api failed ", str(e))


def crawl_some_saglikgov():
    """Crawl source : https://dosyamerkez.saglik.gov.tr/Eklenti/43243/0/zararli-url-listesi.txt
    Response data format : txt
    Update Rate : Unknown
    """
    logging.info("----------- some_saglikgov start -----------")

    try:
        r = get_request(
            SOME_SAGLIKGOV,
            HEADERS,
        )
        if r.status_code != 200:
            logging.warn("some_saglikgov stopped : http status not 200")
            return
    except Exception as e:
        logging.warn("some_saglikgov data crawl  failed ", str(e))
    users_data = []
    lines = r.text.split("\n")
    logging.info("Crawling some_saglikgov found : " + str(len(lines)))
    try:
        for line in lines:
            data = {"resource": "some_saglikgov", "phish_link": line}
            users_data.append(data)
            if len(users_data) % 10000 == 0:
                bulk_insert_users(users_data)
                users_data = []

        # if data count under 10k insert anyway
        bulk_insert_users(users_data)
    except Exception as e:
        logging.warn("some_saglikgov parse feed and send to api failed ", str(e))


def crawl_phishhunt():
    """Crawl source : https://phishunt.io/feed.txt
    Response data format : txt
    Update Rate : Unknown
    """
    logging.info("----------- phishhunt start -----------")
    try:
        r = get_request(
            PHISHHUNT,
            HEADERS,
        )
        if r.status_code != 200:
            logging.warn("phishhunt stopped : http status not 200")
            return
    except Exception as e:
        logging.warn("phishhunt data crawl  failed ", str(e))
    users_data = []
    lines = r.text.split("\n")
    logging.info("Crawling some_saglikgov found : " + str(len(lines)))
    try:
        for line in r.text.split("\n"):
            data = {"resource": "phishhunt", "phish_link": line}
            users_data.append(data)
            if len(users_data) % 10000 == 0:
                bulk_insert_users(users_data)
                users_data = []

        # if data count under 10k insert anyway
        bulk_insert_users(users_data)
    except Exception as e:
        logging.warn("phishhunt parse feed and send to api failed ", str(e))
