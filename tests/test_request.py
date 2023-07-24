from phish_track.crawler.http.request import *
import json



def test_get_request():
    r = get_request("http://ifconfig.me/all.json",{"User-Agent":"test"})
    json_data = json.load(r.text)
    
    assert r.status_code == 200