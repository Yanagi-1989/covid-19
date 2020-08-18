from flask import Flask, jsonify, render_template

from db import PatientsModel
from util import gen_weekly_num_lists, gen_header_dates, gen_weekly_totals

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False
app.config["JSON_SORT_KEYS"] = False


@app.route("/calendar/<prefecture_code>", methods=["GET"])
def api_calendar(prefecture_code):
    """カレンダー生成に必要な情報を返却するAPI.

    Parameters
    ----------
    prefecture_code: 都道府県コード"""

    if prefecture_code not in ("13", ):
        return jsonify([])

    records = PatientsModel.fetch_num(prefecture_code)

    if not len(records):
        return jsonify([])

    weekly_num_lists = gen_weekly_num_lists(records)
    header_dates = gen_header_dates(records[0].publication_date,
                                    records[len(records) - 1].publication_date)
    totals = gen_weekly_totals(weekly_num_lists)

    return jsonify(
        [{"header_date": item[0],
          "num_list": item[1],
          "total": item[2]}
         for item in list(zip(header_dates, weekly_num_lists, totals))]
    )


@app.route("/prefectures", methods=["GET"])
def api_prefectures():
    """地域選択用セレクトボックスにて使用する地域情報を返却するAPI"""

    return jsonify([
        {"prefecture_name": "東京", "prefecture_code": 13},
        # 東京以外はまだ未実装
        # {"prefecture_name": "神奈川", "prefecture_code": 12}
    ])


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run()
