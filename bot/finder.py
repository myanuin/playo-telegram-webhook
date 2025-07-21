import requests
import datetime
import pytz
from dateutil import parser
from math import radians, cos, sin, asin, sqrt

def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in km
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2)**2
    c = 2 * asin(sqrt(a))
    return round(R * c, 1)

def fetch_football_games(config):
    timezone = pytz.timezone(config["timezone"])
    now = datetime.datetime.now(timezone)
    today_date = now.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    url = "https://api.playo.io/activity-public/list/location"
    payload = {
        "lat": config["lat"],
        "lng": config["lng"],
        "cityRadius": config["radius"],
        "gameTimeActivities": False,
        "page": 0,
        "lastId": "",
        "sportId": [config["sport"]],
        "booking": False,
        "date": [today_date]
    }

    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    data = response.json()

    activities = data.get("data", {}).get("activities", [])
    time_slots = [("18:00", "19:00"), ("19:00", "20:00"), ("20:00", "21:00"), ("21:00", "22:00")]

    matches = []
    for start_str, end_str in time_slots:
        desired_start = datetime.datetime.strptime(start_str, "%H:%M").time()

        for activity in activities:
            try:
                start = parser.parse(activity["startTime"]).astimezone(timezone)
                end = parser.parse(activity["endTime"]).astimezone(timezone)
            except:
                continue

            duration = (end - start).seconds // 60
            if start.hour != desired_start.hour or duration < 50 or duration > 70:
                continue

            if activity.get("full"):
                continue

            distance = haversine(config["lat"], config["lng"], activity.get("lat", 0), activity.get("lng", 0))

            matches.append({
                "venue": activity.get("venueName", "Unknown"),
                "start": start.strftime("%I:%M %p"),
                "end": end.strftime("%I:%M %p"),
                "players": f"{activity.get('joineeCount', 0)}/{activity.get('maxPlayers', '∞')}",
                "host": activity.get("userInfo", [{}])[0].get("fName", "Unknown"),
                "link": f"https://playo.co/match/{activity['id']}",
                "distance": distance
            })

    return matches
