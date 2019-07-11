import json
from datetime import datetime, timedelta


def init_params():
    return {
        "init": False,
    }


def create_demo_data():
    with open("data/demo.json") as f:
        _data = json.load(f)
    return _data


def get_jpn_datetime(dts: str):
    return datetime.strptime(dts, '%Y-%m-%dT%H:%M:%S.000Z') + timedelta(hours=9)


def create_params(data):
    tags = data["items"][0]["snippet"]["tags"]
    title = data["items"][0]["snippet"]["title"]
    _id = data["items"][0]["id"]
    _url = "https://www.youtube.com/watch?v=" + _id
    published_at = get_jpn_datetime(data["items"][0]["snippet"]["publishedAt"])
    channel = data["items"][0]["snippet"]["channelTitle"]
    thumbnail = data["items"][0]["snippet"]["thumbnails"]["medium"]["url"]
    channel_id = data["items"][0]["snippet"]["channelId"]
    return {
        "init": True,
        "title": title,
        "url": _url,
        "published_at": published_at,
        "channel": channel,
        "thumbnail": thumbnail,
        "tags": tags,
        "id": _id,
        "channel_id": channel_id,
    }