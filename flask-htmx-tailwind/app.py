from flask import Flask, render_template, request, abort
from pathlib import Path
from db import db
import models

app = Flask(__name__, instance_relative_config=True)

Path(app.instance_path).mkdir(parents=True, exist_ok=True)
db_path = Path(app.instance_path) / "app.db"
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path.as_posix()}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

@app.get("/")
def home():
    return render_template("index.html")

@app.get("/dynasties")
def dynasties_list():
    from models import Dynasty
    items = Dynasty.query.order_by(Dynasty.created_at.desc()).all()
    return render_template("partials/_dynasty_list.html", dynasties=items)

@app.post("/dynasties")
def dynasties_create():
    from models import Dynasty
    name = request.form.get("name", "").strip()
    commish = request.form.get("commissioner", "").strip()

    if not name or not commish:
        return (
            '<p class="mt-2 text-sm text-red-400">Name and commissioner are required.</p>',
            400,
        )

    d = Dynasty(name=name, commissioner=commish)
    db.session.add(d)
    db.session.commit()
    return render_template("partials/_dynasty_row.html", d=d)

@app.delete("/dynasties/<int:did>")
def dynasties_delete(did: int):
    from models import Dynasty
    d = Dynasty.query.get(did)
    if not d:
        abort(404)
    db.session.delete(d)
    db.session.commit()
    return ("", 204)
