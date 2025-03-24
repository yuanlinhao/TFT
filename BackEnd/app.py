from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import os
from flask_cors import CORS
from sqlalchemy import text

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Allow all origins

# Configure PostgreSQL connection
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://yuanlinhao@localhost/tft_database"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {"pool_pre_ping": True}  # Prevent connection loss issues

db = SQLAlchemy(app, session_options={"autoflush": False})

with app.app_context():
    db.reflect()

# Define Champion model
class Champion(db.Model):
    __tablename__ = 'champions'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    cost = db.Column(db.Integer, nullable=False)
    health = db.Column(db.Integer, nullable=False)
    attack_damage = db.Column(db.Integer, nullable=False)
    attack_speed = db.Column(db.Float, nullable=False)
    armor = db.Column(db.Integer, nullable=False)
    magic_resist = db.Column(db.Integer, nullable=False)
    ability_name = db.Column(db.String, nullable=False)
    ability_description = db.Column(db.Text, nullable=False)
    ability_damage = db.Column(db.Integer, nullable=False)
    mana_cost = db.Column(db.Integer, nullable=False)
    starting_mana = db.Column(db.Integer, nullable=False)

# Define Item model
class Item(db.Model):
    __tablename__ = 'items'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    ability_power = db.Column(db.Integer, default=0)
    mana = db.Column(db.Integer, default=0)
    crit_chance = db.Column(db.Float, default=0)
    crit_damage = db.Column(db.Float, default=0)
    bonus_effect = db.Column(db.Text, nullable=True)

# Route to fetch all champions with optional filtering
@app.route("/champions", methods=["GET"])
def get_champions():
    query = Champion.query
    name_filter = request.args.get("name")
    cost_filter = request.args.get("cost")

    if name_filter:
        query = query.filter(Champion.name.ilike(f"%{name_filter}%"))
    if cost_filter:
        query = query.filter(Champion.cost == int(cost_filter))
    
    champions = query.all()
    return jsonify([{ 
        "id": c.id,
        "name": c.name,
        "cost": c.cost,
        "health": c.health,
        "attack_damage": c.attack_damage,
        "attack_speed": c.attack_speed,
        "armor": c.armor,
        "magic_resist": c.magic_resist,
        "ability_name": c.ability_name,
        "ability_description": c.ability_description,
        "ability_damage": c.ability_damage,
        "mana_cost": c.mana_cost,
        "starting_mana": c.starting_mana
    } for c in champions])

# Route to fetch all items with optional filtering
@app.route("/items", methods=["GET"])
def get_items():
    query = Item.query
    name_filter = request.args.get("name")
    ability_power_filter = request.args.get("ability_power")

    if name_filter:
        query = query.filter(Item.name.ilike(f"%{name_filter}%"))
    if ability_power_filter:
        query = query.filter(Item.ability_power >= int(ability_power_filter))
    
    items = query.all()
    return jsonify([{ 
        "id": i.id,
        "name": i.name,
        "ability_power": i.ability_power,
        "mana": i.mana,
        "crit_chance": i.crit_chance,
        "crit_damage": i.crit_damage,
        "bonus_effect": i.bonus_effect
    } for i in items])

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)
