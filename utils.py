import json
from datetime import datetime, timedelta
from googleapiclient.discovery import build

import os
from typing import List

import pandas as pd

from keys import API_KEY

__DEMO_DATA_JSON = "data/demo.json"
__VTUBER_MUSIC_DATA_CSV = "data/vtuber_music.csv"

__DF_COLUMNS = ("vtuber", "music", "original", "collab", "collabVTuber", "id", "channelId", "publishedAt", "memo")

DEVELOPER_KEY = API_KEY
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

def init_params():
    # jinja2レンダリングで使うjsonデータの初期値
    return {
        "init": False,
        "existsUrl": False,
    }


def create_demo_data():
    # デモデータを使う
    with open(__DEMO_DATA_JSON) as f:
        _data = json.load(f)
    return _data


def load_csv_data():
    # csvからdfをロード
    if os.path.exists(__VTUBER_MUSIC_DATA_CSV):
        return pd.read_csv(__VTUBER_MUSIC_DATA_CSV, index_col=0)
    return pd.DataFrame({k: [] for k in __DF_COLUMNS})


def append_data(df: pd.DataFrame, data_list: List):
    # dfにデータを追加
    sr = pd.Series(data_list, index=__DF_COLUMNS)
    return df.append(sr, ignore_index=True)


def save_csv(df: pd.DataFrame):
    # csvにdfを保存
    df.to_csv(__VTUBER_MUSIC_DATA_CSV)


def get_jpn_datetime(dts: str):
    # ISOなんとか時間から日本の標準時間にする
    return datetime.strptime(dts, '%Y-%m-%dT%H:%M:%S.000Z') + timedelta(hours=9)


def create_params(data):
    # youtube apiから来たjsonデータから必要なところだけ取り出す
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
        "existsUrl": False,
    }

def exists_id(df: pd.DataFrame, _id: str):
    # dfにidが存在するか
    return _id in df["id"].tolist()


def search_youtube(_id: str):
    # YouTube Data APIを叩く
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                developerKey=DEVELOPER_KEY)
    return youtube.videos().list(
        id=_id,
        part="id,snippet,statistics",
        maxResults=1
    ).execute()


if __name__ == '__main__':
    import json
    data = search_youtube("dkWh74qgf8U")
    print(json.dumps(data, indent=2))
    print(create_params(data))
