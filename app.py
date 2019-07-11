from flask import Flask, request
from flask import render_template

from utils import init_params, create_params, create_demo_data


app = Flask(__name__)


@app.route('/', methods=["GET"])
def index():
    url = request.args.get("url", "")
    if url == "":
        vtuber = request.args.get("vtuber", "")
        if vtuber == "":
            # 一番最初
            params = init_params()
            return render_template("index.html", params=params)

        print(request.args)
        params = init_params()
        return render_template("index.html", params=params)
    else:
        # URLが入力された時
        data = create_demo_data()
        params = create_params(data)
        print(params)
        return render_template("index.html", params=params)
    # tags = demo["items"][0]["snippet"]["tags"]
    # title = demo["items"][0]["snippet"]["title"]
    # _url = "https://www.youtube.com/watch?v=" + demo["items"][0]["id"]
    # published_at = datetime.strptime(demo["items"][0]["snippet"]["publishedAt"], '%Y-%m-%dT%H:%M:%S.000Z') + timedelta(hours=9)
    # channel = demo["items"][0]["snippet"]["channelTitle"]
    # thumbnail = demo["items"][0]["snippet"]["thumbnails"]["medium"]["url"]
    # if request.method == "GET":
    #     url = request.args.get("url", "")
    #     print("url: \"" + url + "\"")
    #     return render_template("index.html", tags=tags, url=url,
    #                            params={"title": title, "url": _url, "published_at": published_at, "channel": channel,
    #                                    "thumbnail": thumbnail})
    # return render_template("index.html", tags=tags)


if __name__ == '__main__':
    app.run(debug=True)
