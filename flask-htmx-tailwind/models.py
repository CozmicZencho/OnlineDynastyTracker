# models.py
from db import db
from datetime import datetime
from enum import Enum

# ---- Enums ----
class Role(str, Enum):
    NORMAL = "NORMAL"
    COMMISSIONER = "COMMISSIONER"
    OWNER = "OWNER"

class Designation(str, Enum):
    HC = "HC"
    OC = "OC"
    DC = "DC"

# ---- Core tables ----
class Dynasty(db.Model):
    __tablename__ = "dynasties"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    members = db.relationship("DynastyMember", back_populates="dynasty", cascade="all, delete-orphan")

    def member_count(self) -> int:
        return len(self.members)

    def owner(self):
        return next((m for m in self.members if m.role == Role.OWNER.value), None)

class Player(db.Model):
    """
    A person who can join dynasties.
    You can later add auth fields; for now just display_name is enough.
    """
    __tablename__ = "players"
    id = db.Column(db.Integer, primary_key=True)
    display_name = db.Column(db.String(120), nullable=False, unique=True)  # e.g., "Cameron"
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    memberships = db.relationship("DynastyMember", back_populates="player", cascade="all, delete-orphan")

class DynastyMember(db.Model):
    """
    Membership of a Player in a Dynasty, with team + role + designation.
    Enforces:
      - Up to 16 members (app-side check)
      - Exactly one owner (app-side check)
      - Team uniqueness per dynasty (DB constraint)
      - Each member has a team + designation
    """
    __tablename__ = "dynasty_members"

    id = db.Column(db.Integer, primary_key=True)
    dynasty_id = db.Column(db.Integer, db.ForeignKey("dynasties.id", ondelete="CASCADE"), nullable=False)
    player_id = db.Column(db.Integer, db.ForeignKey("players.id", ondelete="CASCADE"), nullable=False)

    team = db.Column(db.String(80), nullable=False)  # e.g., "TAMU", "LSU", "ORE", or full team name
    designation = db.Column(db.Enum(Designation), nullable=False, default=Designation.HC)
    role = db.Column(db.Enum(Role), nullable=False, default=Role.NORMAL)

    joined_at = db.Column(db.DateTime, default=datetime.utcnow)

    dynasty = db.relationship("Dynasty", back_populates="members")
    player = db.relationship("Player", back_populates="memberships")

    __table_args__ = (
        # A dynasty cannot have two members with the same team
        db.UniqueConstraint("dynasty_id", "team", name="uq_dynasty_team_once"),
        # A player shouldn't be duplicated in the same dynasty
        db.UniqueConstraint("dynasty_id", "player_id", name="uq_player_once_in_dynasty"),
    )

class TeamPlayer(db.Model):
    __tablename__ = "team_players"
    id = db.Column(db.Integer, primary_key=True)

    # link to a dynasty member (the human playing this team)
    member_id = db.Column(
        db.Integer,
        db.ForeignKey("dynasty_members.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # basic player info (extend later as needed)
    name = db.Column(db.String(100), nullable=False)
    position = db.Column(db.String(10), nullable=False)   # e.g., QB, RB, WR, TE, OL, DL, LB, CB, S, K, P
    overall = db.Column(db.Integer)                        # optional rating
    year = db.Column(db.String(10))                        # e.g., FR, SO, JR, SR, RS-FR, etc.

    dynasty_member = db.relationship("DynastyMember", backref="team_players")
