from flask import Flask, render_template, request, abort, redirect, url_for, jsonify
from pathlib import Path
from db import db

app = Flask(__name__, instance_relative_config=True)

Path(app.instance_path).mkdir(parents=True, exist_ok=True)
db_path = Path(app.instance_path) / "app.db"
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path.as_posix()}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

from models import Dynasty, Player, DynastyMember, Role, Designation, TeamPlayer  

with app.app_context():
    db.create_all()

@app.get("/")
def home():
    return render_template("index.html")

@app.get("/dynasties")
def dynasties_list():
    items = Dynasty.query.order_by(Dynasty.created_at.desc()).all()
    return render_template("partials/_dynasty_list.html", dynasties=items)

# ---- Dynasty CRUD ----
@app.get("/dynasties/new")
def dynasties_new():
    return render_template("partials/_dynasty_form.html")

@app.post("/dynasties")
def dynasties_create():
    name = (request.form.get("name") or "").strip()
    owner_name = (request.form.get("owner_name") or request.form.get("commissioner") or "").strip()
    owner_team = (request.form.get("owner_team") or request.form.get("team") or "").strip()
    owner_designation = (request.form.get("owner_designation") or "HC").strip()

    if not name or not owner_name or not owner_team:
        return ('<p class="text-red-400 text-sm mt-2">Dynasty name, owner name, and owner team are required.</p>', 400)

    d = Dynasty(name=name)
    db.session.add(d); db.session.flush()

    p = Player.query.filter_by(display_name=owner_name).first()
    if not p:
        p = Player(display_name=owner_name)
        db.session.add(p); db.session.flush()

    m = DynastyMember(
        dynasty_id=d.id,
        player_id=p.id,
        team=owner_team,
        designation=Designation(owner_designation),
        role=Role.OWNER,
    )
    db.session.add(m); db.session.commit()

    return render_template("partials/_dynasty_row.html", d=d)

@app.delete("/dynasties/<int:did>")
def dynasties_delete(did: int):
    d = Dynasty.query.get_or_404(did)
    db.session.delete(d); db.session.commit()
    return ("", 204)

# ---- Roster pages & member management ----
@app.get("/dynasties/<int:did>/roster")
def roster_page(did: int):
    d = Dynasty.query.get_or_404(did)
    members = DynastyMember.query.filter_by(dynasty_id=did).order_by(DynastyMember.joined_at.desc()).all()
    return render_template("roster.html", d=d, members=members, Role=Role, Designation=Designation)

@app.post("/dynasties/<int:did>/members")
def members_add(did: int):
    # ... (your existing logic)
    ...

@app.post("/dynasties/<int:did>/members/<int:mid>/update")
def members_update(did: int, mid: int):
    # ... (your existing logic)
    ...

@app.delete("/dynasties/<int:did>/members/<int:mid>")
def members_delete(did: int, mid: int):
    # ... (your existing logic)
    ...

# ---- Team roster layer (optional, if you added TeamPlayer) ----
@app.get("/dynasties/<int:did>/members/<int:mid>/team")
def team_roster(did: int, mid: int):
    # ... (your existing logic)
    ...

@app.post("/dynasties/<int:did>/members/<int:mid>/team")
def team_player_add(did: int, mid: int):
    # ... (your existing logic)
    ...

# 5) Main entrypoint (optional, for waitress start)
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        print(f"Database initialized at: {db_path}")
    from waitress import serve
    serve(app, host="127.0.0.1", port=5000)
