from flask import Flask, render_template
from flask import request, jsonify
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///local.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class Entry(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    username = db.Column(db.String(20), nullable=False)
    github_id = db.Column(db.Integer, unique=True)
    image_url = db.Column(db.String(255), nullable=False)
    type = db.Column(db.String(20), nullable=False)
    github_profile = db.Column(db.String(), nullable=False)


def get_paging_params(page):
    arg_limit = request.args.get("limit", 25)
    limit = int(arg_limit)
    offset = (limit * page) - limit
    return limit, offset


@app.route("/")
def index():
    page = request.args.get("page", 1)
    limit, offset = get_paging_params(int(page))
    total = Entry.query.count()
    order_by = request.args.get("order_by", default="id")
    entries = (Entry.query.order_by(
        getattr(Entry, order_by)).offset(offset).limit(limit).all())
    context = {
        'entries': [i.to_dict() for i in entries],
        'page': int(page),
        'limit': int(limit),
        'total': total,
    }
    if request.args.get("format") == 'json':
        return jsonify(context)
    return render_template("index.html", **context)
