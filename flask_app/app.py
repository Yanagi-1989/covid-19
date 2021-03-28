import os

from flask import Flask, jsonify, render_template

from db import PatientsModel
from util import gen_weekly_num_lists, gen_header_dates, gen_weekly_totals

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False
app.config["JSON_SORT_KEYS"] = False

# Flaskの元々の予約語 {{}} は Vue.jsの予約語と被るため、
# Flaskの予約語を変更する
app.jinja_options["variable_start_string"] = "[["
app.jinja_options["variable_end_string"] = "]]"


@app.route("/calendar/<prefecture_code>", methods=["GET"])
def api_calendar(prefecture_code):
    """カレンダー生成に必要な情報を返却するAPI.

    Parameters
    ----------
    prefecture_code: 都道府県コード"""

    # 全国 + 47都道府県 以外のコードが要求された場合は空を返却
    if prefecture_code not in [f"{idx:02d}" for idx in range(0, 48)]:
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
        # 日本全国を指す都道府県コードを便宜上'00'としている
        {"prefecture_name": "全国", "prefecture_code": "00"},
        # 以下、47都道府県
        {"prefecture_name": "北海道", "prefecture_code": "01"},
        {"prefecture_name": "青森県", "prefecture_code": "02"},
        {"prefecture_name": "岩手県", "prefecture_code": "03"},
        {"prefecture_name": "宮城県", "prefecture_code": "04"},
        {"prefecture_name": "秋田県", "prefecture_code": "05"},
        {"prefecture_name": "山形県", "prefecture_code": "06"},
        {"prefecture_name": "福島県", "prefecture_code": "07"},
        {"prefecture_name": "茨城県", "prefecture_code": "08"},
        {"prefecture_name": "栃木県", "prefecture_code": "09"},
        {"prefecture_name": "群馬県", "prefecture_code": "10"},
        {"prefecture_name": "埼玉県", "prefecture_code": "11"},
        {"prefecture_name": "千葉県", "prefecture_code": "12"},
        {"prefecture_name": "東京都", "prefecture_code": "13"},
        {"prefecture_name": "神奈川県", "prefecture_code": "14"},
        {"prefecture_name": "新潟県", "prefecture_code": "15"},
        {"prefecture_name": "富山県", "prefecture_code": "16"},
        {"prefecture_name": "石川県", "prefecture_code": "17"},
        {"prefecture_name": "福井県", "prefecture_code": "18"},
        {"prefecture_name": "山梨県", "prefecture_code": "19"},
        {"prefecture_name": "長野県", "prefecture_code": "20"},
        {"prefecture_name": "岐阜県", "prefecture_code": "21"},
        {"prefecture_name": "静岡県", "prefecture_code": "22"},
        {"prefecture_name": "愛知県", "prefecture_code": "23"},
        {"prefecture_name": "三重県", "prefecture_code": "24"},
        {"prefecture_name": "滋賀", "prefecture_code": "25"},
        {"prefecture_name": "京都", "prefecture_code": "26"},
        {"prefecture_name": "大阪府", "prefecture_code": "27"},
        {"prefecture_name": "兵庫県", "prefecture_code": "28"},
        {"prefecture_name": "奈良県", "prefecture_code": "29"},
        {"prefecture_name": "和歌山県", "prefecture_code": "30"},
        {"prefecture_name": "鳥取県", "prefecture_code": "31"},
        {"prefecture_name": "島根県", "prefecture_code": "32"},
        {"prefecture_name": "岡山県", "prefecture_code": "33"},
        {"prefecture_name": "広島県", "prefecture_code": "34"},
        {"prefecture_name": "山口県", "prefecture_code": "35"},
        {"prefecture_name": "徳島県", "prefecture_code": "36"},
        {"prefecture_name": "香川県", "prefecture_code": "37"},
        {"prefecture_name": "愛媛県", "prefecture_code": "38"},
        {"prefecture_name": "高知県", "prefecture_code": "39"},
        {"prefecture_name": "福岡県", "prefecture_code": "40"},
        {"prefecture_name": "佐賀県", "prefecture_code": "41"},
        {"prefecture_name": "長崎県", "prefecture_code": "42"},
        {"prefecture_name": "熊本県", "prefecture_code": "43"},
        {"prefecture_name": "大分県", "prefecture_code": "44"},
        {"prefecture_name": "宮崎県", "prefecture_code": "45"},
        {"prefecture_name": "鹿児島県", "prefecture_code": "46"},
        {"prefecture_name": "沖縄県", "prefecture_code": "47"}
    ])


@app.route("/")
def index():
    return render_template("index.html", domain=os.environ["DOMAIN"])


if __name__ == "__main__":
    app.run()
