import json
import sys
from flask import Flask, jsonify, render_template
from . import db
from . import utils

app = Flask(__name__)


# Normally I'd put the config in a file, but for something
# this basic, manually setting the values is OK
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_SORT_KEYS'] = False
app.json_encoder = utils.CustomJSONEncoder
db.db.init_app(app)


@app.route('/')
def main():
    with open('risks/templates/index.html') as f:
        return f.read()


@app.route('/api/v1/risktype/<type>')
def v1_risk(type):
    try:
        risk_type = db.RiskType.query.filter(db.RiskType.name==type).one()
    except:
        result = jsonify({'status_code': 404, 'message': 'No result found'})
        result.status_code = 404
        return result
    return jsonify(risk_type)


@app.route('/api/v1/risktypes')
def v1_risks():
    risk_types = db.RiskType.query.all()
    return jsonify(risk_types)


def run():
    # Normally I'd use argparse, click, or some other argument parsing
    # library. But for something this simple, just checking sys.argv is
    # fine.
    if '--create-all' in sys.argv:
        db.create_all(app)

    if '--add-samples' in sys.argv:
        db.add_samples(app)

    app.run(host='127.0.0.1', port=5432)
