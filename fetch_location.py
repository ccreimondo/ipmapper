#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from pymongo import MongoClient, DESCENDING
from secret import server
from json import loads

def fast():
    db = MongoClient(server.MONGODB_DEV_URI)["mirrors"]
    find_law = {
        "hits": { "$gt": 0 },
        "pages": { "$gt": 0 },
        "bandwidth": { "$gt": 0}
    }
    inven_cursor = db["ip1_5"].find(find_law)
    re_currsor = inven_cursor.sort("bandwidth", DESCENDING).limit(2000)
    pcoll = db["ip1_5_s"]
    for e in re_currsor:
        pcoll.insert_one(e)


def fetch():
    qurl = "http://freeapi.ipip.net"
    db = MongoClient(server.MONGODB_DEV_URI)["mirrors"]
    cursor = db["ip1_5_s"].find().sort("bandwidth", DESCENDING)
    for e in cursor:
        if "location" in e.keys(): continue
        re = requests.get('/'.join([qurl, e["host"]]))
        if re.status_code != 200:
            raise Exception(' '.join(["Fetch ip location error", str(re.status_code)]))
        e["location"] = loads(re.text)
        db["ip1_5_s"].save(e)


def figure():
    db = MongoClient(server.MONGODB_DEV_URI)["mirrors"]
    # db = MongoClient("localhost", 27017)["mirrors"]
    cursor = db["ip1_5_s"].find()
    re = {u"重庆大学": 0, u"教育网": 0}
    for e in cursor:
        location = e["location"]
        if location[0] not in re.keys():
            re[location[0]] = 0
        if location[1] not in re.keys():
            re[location[1]] = 0
        if location[0] == location[1]:
            re[location[0]] += 1
        else:
            re[location[0]] += 1
            re[location[1]] += 1
        if location[3] == u"重庆大学":
            re[location[3]] += 1
        if location[4] == u"教育网":
            re[location[4]] += 1
    rank = sorted(re.items(), key=lambda x: x[1], reverse=True)

    with open("rank.txt", 'w') as outfile:
        for e in rank:
            outfile.write(e[0].encode("utf-8"))
            outfile.write(''.join([' ', str(e[1]), '\n']))

def main():
    # fast()
    # fetch()
    # figure()


if __name__ == "__main__":
    main()
