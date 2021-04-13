from flask import Flask, render_template
from flask import request
import dataset

app = Flask(__name__)
db = dataset.connect("sqlite:///local.db")
LIMIT = 25


def get_paging_params(page):
    limit = LIMIT
    offset = (limit*int(page)) - limit;
    return {'_limit': limit, '_offset': offset}


@app.route("/")
def index():
    page = request.args.get("page", 1)
    params = get_paging_params(page)
    total = db["entries"].count()
    entries = db["entries"].all(**params)
    context = {
        'entries': entries,
        'page': page,
        'pages': range(total//LIMIT)
    }
    return render_template("index.html", **context)


