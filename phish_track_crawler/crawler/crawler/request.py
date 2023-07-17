import httpx
import logging as _logging


timeout = 30


def get_request(url, head):
    try:
        with httpx.Client(headers=head, timeout=timeout) as client:
            response = client.get(url, follow_redirects=True)
    except httpx.RequestError as e:
        _logging.warn("Get request error " + str(e))
        return None
    return response


def post_request(url, data, head):
    try:
        with httpx.Client(headers=head, timeout=timeout) as client:
            response = client.post(url, follow_redirects=True, json=data)
    except Exception as e:
        _logging.warn("post request error " + str(e))
        return

    return response
