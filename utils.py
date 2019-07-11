import json
from datetime import datetime, timedelta

import os
from typing import List

import pandas as pd

__DEMO_DATA_JSON = "data/demo.json"
__VTUBER_MUSIC_DATA_CSV = "data/vtuber_music.csv"

__DF_COLUMNS = ("vtuber", "music", "original", "collab", "id", "channelId", "publishedAt", "memo")


def init_params():
    return {
        "init": False,
    }


def create_demo_data():
    with open(__DEMO_DATA_JSON) as f:
        _data = json.load(f)
    return _data


def load_csv_data():
    if os.path.exists(__VTUBER_MUSIC_DATA_CSV):
        return pd.read_csv(__VTUBER_MUSIC_DATA_CSV)
    return pd.DataFrame({k: [] for k in __DF_COLUMNS})


def append_data(df: pd.DataFrame, data_list: List):
    sr = pd.Series(data_list, index=__DF_COLUMNS)
    return df.append(sr, ignore_index=True)


def save_csv(df: pd.DataFrame):
    df.to_csv(__VTUBER_MUSIC_DATA_CSV)


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


def exists_id(df: pd.DataFrame, _id: str):
    return df["id"].isin(_id)
