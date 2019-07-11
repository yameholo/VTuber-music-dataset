from flask import Flask, request
from flask import render_template
from werkzeug.datastructures import ImmutableMultiDict

from utils import init_params, create_params, create_demo_data, load_csv_data, append_data, save_csv

app = Flask(__name__)
DF = load_csv_data()
print(DF)


def save_data(data):
    global DF
    data_list = parse_data(data)
    print(data_list)
    DF = append_data(DF, data_list)
    save_csv(DF)


def parse_data(data: ImmutableMultiDict):
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
        data = create_demo_data()
        params = create_params(data)
        print(params)
        return render_template("index.html", params=params)


if __name__ == '__main__':
    app.run(debug=True)
