from flask import Flask, render_template
from flask import request, jsonify
import dataset

app = Flask(__name__)


def get_paging_params(page):
    arg_limit = request.args.get("limit", 25)
    limit = int(arg_limit)
    offset = (limit*page) - limit;
    return {'_limit': limit, '_offset': offset}


@app.route("/")
def index():
    db = dataset.connect("sqlite:///local.db")
    page = request.args.get("page", 1)
    params = get_paging_params(int(page))
    total = db["entries"].count()
    limit = params.get("_limit")
    params.update({
        'order_by': ['id', 'type']
    })
    entries = db["entries"].all(**params)
    context = {
        'entries': list(entries),
        'page': int(page),
        'limit': int(limit),
        'total': total,
    }
    if request.args.get("format") == 'json':
        return jsonify(context)
    return render_template("index.html", **context)


