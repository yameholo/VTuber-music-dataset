from flask import Flask, request
from flask import render_template
from werkzeug.datastructures import ImmutableMultiDict

from utils import init_params, create_params, create_demo_data, load_csv_data, append_data, save_csv, exists_id

app = Flask(__name__)
DF = load_csv_data()
print(DF.head())


def save_data(data):
    # dfを更新してcsvに保存する
    global DF
    data_list = parse_data(data)
    DF = append_data(DF, data_list)
    save_csv(DF)


def parse_data(data: ImmutableMultiDict):
    # formから来たデータをパースする
    return [
        data.get("vtuber") if data.get("isOtherVTuber") is None else data.get("OtherVTuber"),
        data.get("music") if data.get("isOtherMusic") is None else data.get("OtherMusic"),
        data.get("original") if data.get("isOtherOriginal") is None else data.get("OtherOriginal"),
        "True" if data.get("isCollab") == "yes" else "False",
        data.get("collabVTuber"),
        data.get('id'),
        data.get("channelId"),
        data.get("publishedAt"),
        data.get("memo")
    ]



@app.route('/', methods=["GET"])
def index():
    url = request.args.get("url", "")
    if url == "":
        vtuber = request.args.get("vtuber", "")
        if vtuber != "":
            print(request.args)
            save_data(request.args)

        params = init_params()
        return render_template("index.html", params=params)
    else:
        # URLが入力された時
        _id = url.split("?v=")[-1]
        if exists_id(DF, _id):
            params = init_params()
            params["existsUrl"] = True
            params["url"] = url
            print(params)
            return render_template("index.html", params=params)
        data = create_demo_data()
        params = create_params(data)
        return render_template("index.html", params=params)


if __name__ == '__main__':
    app.run(debug=True)
