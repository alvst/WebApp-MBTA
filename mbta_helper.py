import requests
import urllib.request
import pprint
import json
import math
def find_stop_near(nearby, check):
    # print(":t")
    # print(ebus, lbus, train)
    # print(checkers)
    info = find_location(nearby)
    if False in info:
        return find_stop(info, check)
    return ["Sorry there are no stops around you 😞."]

def find_location(nearby):
    key = 'sV2BLO1vtZTu2pXfQ0Wt0QBk3tM6WL1m'
    nearby = nearby.replace(' ', '%20')
    url = f'http://www.mapquestapi.com/geocoding/v1/address?key={key}&location={nearby},MA'
    try:
        with urllib.request.urlopen(url) as p:
            data = json.load(p)
        for locations in range(len(data["results"][0]["locations"])):
            country = data["results"][0]["locations"][locations]["adminArea1"]
            state = data["results"][0]["locations"][locations]["adminArea3"]
            if country == "US" and state == "MA":
                break
            else:
                if locations == len(data["results"][0]["locations"])-1:
                    return [True]
        latitude = data["results"][0]["locations"][locations]["latLng"]["lat"]
        longitude = data["results"][0]["locations"][locations]["latLng"]["lng"]
        return [False, latitude, longitude]

    except Exception as e:
        return {True, 0, 0}

def find_stop(info, check):
    lat = info[1]
    long = info[2]
    url = f'https://api-v3.mbta.com/stops?filter%5Blatitude%5D={lat}&filter%5Blongitude%5D={long}'
    # try:
    with urllib.request.urlopen(url) as p:
        data = json.load(p)
    stop_num = 0
    small_hyp = 10000
    find = []
    for stops in range(len(data["data"])):
        ch = data["data"][stops]["relationships"]["zone"]["data"]
        if len(check) == 1 or len(check) == 2:
            if ch != None:
                if "RapidTransit" in check:
                    if data["data"][stops]["relationships"]["zone"]["data"]["id"] == "RapidTransit":
                        find.append(stops)
                if "LocalBus" in check:
                    # print(data["data"][stops]["relationships"]["zone"]["data"]["id"])
                    if data["data"][stops]["relationships"]["zone"]["data"]["id"] == "LocalBus":
                        find.append(stops)
                if "ExpressBus-Downtown" in check:
                    # print(data["data"][stops]["relationships"]["zone"]["data"]["id"])
                    if data["data"][stops]["relationships"]["zone"]["data"]["id"] == "ExpressBus-Downtown":
                        find.append(stops)
                    # print(find)
            else: 
                continue
        else:
            find.append(stops)

    for stop_f in range(len(find)):
        nearby_lat = data["data"][stop_f]["attributes"]["latitude"] - lat
        nearby_long = data["data"][stop_f]["attributes"]["longitude"] - long
        hyp = math.sqrt(nearby_lat **2 + nearby_long **2)
        # print(f'{hyp} of {stop_f} vs {small_hyp} of {stop_num}')
        if hyp < small_hyp:
            small_hyp = hyp
            stop_num = stop_f
    closest_stop = data["data"][stop_num]["attributes"]["name"]
    wheelchair = data["data"][stop_num]["attributes"]["wheelchair_boarding"]
    if wheelchair == 0:
        wheelchair = "No information"
    if wheelchair == 1:
        wheelchair = "Accessible"
    if wheelchair == 2:
        wheelchair = "Inaccessible"
    print(closest_stop)
    return [closest_stop, wheelchair]