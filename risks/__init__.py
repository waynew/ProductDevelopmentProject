import json
from collections import OrderedDict
from flask import Flask, jsonify, render_template
from flask.json import JSONEncoder
from . import db

app = Flask(__name__)


class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        try:
            if isinstance(obj, db.RiskField):
                field = OrderedDict(
                    name=obj.type.name,
                    label=obj.label,
                    type=obj.type.type,
                )
                if obj.type.type == 'enum':
                    field['options'] = [json.loads(v.value) for v in obj.type.values]
                return field
            elif isinstance(obj, db.RiskType):
                type = OrderedDict(type=obj.name, label=obj.label, fields=obj.fields)
                return type
        except TypeError:
            pass
        return super().default(obj)



# Normally I'd put the config in a file, but for something
# this basic, manually setting the values is OK
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_SORT_KEYS'] = False
app.json_encoder = CustomJSONEncoder
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
    app.logger.debug(risk_types)
    return jsonify(risk_types)


def run():
    with app.app_context():
        db.db.create_all()
        db.db.session.add(db.RiskFieldType(
            name='first_name',
            type='text',
        ))
        db.db.session.add(db.RiskFieldType(
            name='points',
            type='enum',
        ))
        db.db.session.add(db.RiskEnumValue(
            risk_type_name='points',
            value=json.dumps(1),
        ))
        db.db.session.add(db.RiskEnumValue(
            risk_type_name='points',
            value=json.dumps(2),
        ))
        db.db.session.add(db.RiskEnumValue(
            risk_type_name='points',
            value=json.dumps(3),
        ))
        db.db.session.add(db.RiskFieldType(
            name='salutation',
            type='enum',
        ))
        db.db.session.add(db.RiskEnumValue(
            risk_type_name='salutation',
            value=json.dumps('Mr.'),
        ))
        db.db.session.add(db.RiskEnumValue(
            risk_type_name='salutation',
            value=json.dumps('Mrs.'),
        ))
        db.db.session.add(db.RiskEnumValue(
            risk_type_name='salutation',
            value=json.dumps('Ms.'),
        ))
        db.db.session.add(db.RiskEnumValue(
            risk_type_name='salutation',
            value=json.dumps('Dr.'),
        ))
        db.db.session.add(db.RiskEnumValue(
            risk_type_name='salutation',
            value=json.dumps('Hon.'),
        ))
        db.db.session.add(db.RiskFieldType(
            name='address',
            type='text',
        ))
        db.db.session.add(db.RiskFieldType(
            name='event_name',
            type='text',
        ))
        db.db.session.add(db.RiskFieldType(
            name='date',
            type='date',
        ))
        db.db.session.add(db.RiskFieldType(
            name='age',
            type='number',
        ))
        db.db.session.add(db.RiskFieldType(
            name='probability',
            type='number',
        ))
        db.db.session.add(db.RiskFieldType(
            name='insured value',
            type='number',
        ))
        db.db.session.add(db.RiskFieldType(
            name='reward value',
            type='number',
        ))
        rt = db.RiskType(
            name='property',
            label='Property',
            description='Real Estate',
        )
        db.db.session.add(rt)
        rt.fields.extend([
            db.RiskField(
                type_name='first_name',
                label="First Name",
            ),
            db.RiskField(
                type_name='address',
                label="Address",
            ),
            db.RiskField(
                type_name='insured value',
                label="Insured Value",
            ),
        ])
        rt = db.RiskType(
            name='hole-in-one',
            label='Hole in One',
            description='Hole-in-One contest',
        )
        rt.fields.extend([
            db.RiskField(
                type_name='salutation',
                label="Salutation",
            ),
            db.RiskField(
                type_name='points',
                label="Points",
            ),
            db.RiskField(
                type_name='event_name',
                label="Event Name",
            ),
            db.RiskField(
                type_name='date',
                label="Event Date",
            ),
            db.RiskField(
                type_name='probability',
                label="Probability",
            ),
            db.RiskField(
                type_name='reward value',
                label="Reward Value",
            ),
        ])
        db.db.session.add(rt)
        db.db.session.commit()
# Fields are bits of data like first name, age, zip code, model, serial number,
# Coverage A limit, or prize dollar amount. Basically any data the carrier 
# would want to collect about the risk. Fields can also be of different types,
# like text, date, number, currency, and so forth.
    app.run(debug=True, host='0.0.0.0', port=5555)
