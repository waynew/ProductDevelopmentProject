import json
from collections import OrderedDict
from flask import Flask, jsonify
from flask.json import JSONEncoder
from . import db

app = Flask(__name__)


class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        try:
            if isinstance(obj, db.RiskField):
                field = OrderedDict(name=obj.type.name, type=obj.type.type)
                if obj.type.type == 'enum':
                    field['options'] = [json.loads(v.value) for v in obj.type.values]
                return field
            elif isinstance(obj, db.RiskType):
                type = OrderedDict(type=obj.name, fields=obj.fields)
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
            name='age',
            type='numeric',
        ))
        db.db.session.add(db.RiskFieldType(
            name='probability',
            type='numeric',
        ))
        db.db.session.add(db.RiskFieldType(
            name='insured value',
            type='numeric',
        ))
        db.db.session.add(db.RiskFieldType(
            name='reward value',
            type='numeric',
        ))
        rt = db.RiskType(
            name='property',
            description='Real Estate',
        )
        db.db.session.add(rt)
        rt.fields.extend([
            db.RiskField(
                type_name='first_name',
            ),
            db.RiskField(
                type_name='address',
            ),
            db.RiskField(
                type_name='insured value',
            ),
        ])
        rt = db.RiskType(
            name='Hole in One',
            description='Hole-in-One contest',
        )
        rt.fields.extend([
            db.RiskField(
                type_name='salutation',
            ),
            db.RiskField(
                type_name='points',
            ),
            db.RiskField(
                type_name='event_name',
            ),
            db.RiskField(
                type_name='probability',
            ),
            db.RiskField(
                type_name='reward value',
            ),
        ])
        db.db.session.add(rt)
        db.db.session.commit()
# Fields are bits of data like first name, age, zip code, model, serial number,
# Coverage A limit, or prize dollar amount. Basically any data the carrier 
# would want to collect about the risk. Fields can also be of different types,
# like text, date, number, currency, and so forth.
    app.run(debug=True, host='0.0.0.0', port=5555)
