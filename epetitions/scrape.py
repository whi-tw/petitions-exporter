import json

from collections import namedtuple

from urllib import parse as urlparse
import requests

from .constants import EPETITIONS_BASEURL


def do_json_request(url: str, params={}) -> json:
    if len(params) > 0:
        pURL = urlparse.urlparse(url)
        qs = dict(urlparse.parse_qsl(pURL.query))
        qs.update(params)
        new_query = urlparse.urlencode(qs)
        pURL = pURL._replace(query=new_query)
        url = urlparse.urlunparse(pURL)
        print(url)
    req = requests.get(
        url
    )

    return req.json()


def get_all(params={}) -> json:
    result = []
    next_page = "{}/epetitions.json".format(
        EPETITIONS_BASEURL)
    if not "_pageSize" in params.keys():
        params["_pageSize"] = 500
    while next_page != "":
        req = do_json_request(url=next_page, params=params)
        result += req["result"]["items"]
        try:
            next_page = req["result"]["next"]
        except KeyError:
            next_page = ""
    return result


def parse_petition(petition: dict) -> namedtuple:
    p_tidied = {k: v for k, v in petition.items() if not k.startswith("_")}
    for k, v in p_tidied.items():
        if isinstance(v, dict):
            p_tidied[k] = v['_value']
    keys = p_tidied.keys()
    p_obj = namedtuple(
        "Petition", keys)(**p_tidied)
    # vals = []
    # for val in petition.values():
    #     if isinstance(val, dict):
    #         vals.append(val["_value"])
    # print(keys)
    # print(vals)
    # p = p_obj(*vals)
    return p_obj
