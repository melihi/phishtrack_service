import logging

import httpx

timeout = 30


def get_request(url, head):
    """ http get request function.
    Args:
        url (str) : url address .
        head (dict) : headers dictionary .
    
    """
    try:
        with httpx.Client(headers=head, timeout=timeout) as client:
            response = client.get(url, follow_redirects=True)
    except httpx.RequestError as e:
        logging.warn("Get request error " + str(e))
        return None
    return response


def post_request(url, data, head):
    try:
        with httpx.Client(headers=head, timeout=timeout) as client:
            response = client.post(url, follow_redirects=True, json=data)
    except Exception as e:
        logging.warn("post request error " + str(e))
        return

    return response
