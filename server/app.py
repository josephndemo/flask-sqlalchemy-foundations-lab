from flask import Flask, jsonify
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)

# Database configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize db
db.init_app(app)

# Initialize migration
migrate = Migrate(app, db)

# ---------------------------------------------------
# Route 1: Get earthquake by ID
# ---------------------------------------------------

@app.route("/earthquakes/<int:id>")
def get_earthquake(id):

    quake = Earthquake.query.filter_by(id=id).first()

    if quake:
        return jsonify({
            "id": quake.id,
            "location": quake.location,
            "magnitude": quake.magnitude,
            "year": quake.year
        }), 200

    return jsonify({
        "message": f"Earthquake {id} not found."
    }), 404


# ---------------------------------------------------
# Route 2: Get earthquakes by minimum magnitude
# ---------------------------------------------------

@app.route("/earthquakes/magnitude/<float:magnitude>")
def get_quakes_by_magnitude(magnitude):

    quakes = Earthquake.query.filter(
        Earthquake.magnitude >= magnitude
    ).all()

    quake_list = []

    for quake in quakes:
        quake_list.append({
            "id": quake.id,
            "location": quake.location,
            "magnitude": quake.magnitude,
            "year": quake.year
        })

    return jsonify({
        "count": len(quake_list),
        "quakes": quake_list
    }), 200


if __name__ == "__main__":
    app.run(port=5555, debug=True)