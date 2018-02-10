import json
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class RiskFieldType(db.Model):
    name = db.Column(db.Text, primary_key=True)
    type = db.Column(db.Text)
    values = db.relationship('RiskEnumValue')


class RiskEnumValue(db.Model):
    risk_type_name = db.Column(db.Text, db.ForeignKey(RiskFieldType.name), primary_key=True)
    value = db.Column(db.Text, primary_key=True)


class RiskField(db.Model):
    type_name = db.Column(db.Text, db.ForeignKey(RiskFieldType.name), primary_key=True)
    risk_type_name = db.Column(db.Text, db.ForeignKey('risk_type.name'), primary_key=True)
    label = db.Column(db.Text)
    type = db.relationship('RiskFieldType')


class RiskType(db.Model):
    name = db.Column(db.Text, primary_key=True)
    label = db.Column(db.Text)
    description = db.Column(db.Text)
    fields = db.relationship('RiskField', backref='risk_type')


def create_all(app):
    with app.app_context():
        db.create_all()
        db.session.commit()


def add_samples(app):
    with app.app_context():
        db.create_all()
        db.session.add(RiskFieldType(
            name='first_name',
            type='text',
        ))
        db.session.add(RiskFieldType(
            name='points',
            type='enum',
        ))
        db.session.add(RiskEnumValue(
            risk_type_name='points',
            value=json.dumps(1),
        ))
        db.session.add(RiskEnumValue(
            risk_type_name='points',
            value=json.dumps(2),
        ))
        db.session.add(RiskEnumValue(
            risk_type_name='points',
            value=json.dumps(3),
        ))
        db.session.add(RiskFieldType(
            name='salutation',
            type='enum',
        ))
        db.session.add(RiskEnumValue(
            risk_type_name='salutation',
            value=json.dumps('Mr.'),
        ))
        db.session.add(RiskEnumValue(
            risk_type_name='salutation',
            value=json.dumps('Mrs.'),
        ))
        db.session.add(RiskEnumValue(
            risk_type_name='salutation',
            value=json.dumps('Ms.'),
        ))
        db.session.add(RiskEnumValue(
            risk_type_name='salutation',
            value=json.dumps('Dr.'),
        ))
        db.session.add(RiskEnumValue(
            risk_type_name='salutation',
            value=json.dumps('Hon.'),
        ))
        db.session.add(RiskFieldType(
            name='address',
            type='text',
        ))
        db.session.add(RiskFieldType(
            name='event_name',
            type='text',
        ))
        db.session.add(RiskFieldType(
            name='date',
            type='date',
        ))
        db.session.add(RiskFieldType(
            name='age',
            type='number',
        ))
        db.session.add(RiskFieldType(
            name='probability',
            type='number',
        ))
        db.session.add(RiskFieldType(
            name='insured value',
            type='number',
        ))
        db.session.add(RiskFieldType(
            name='reward value',
            type='number',
        ))
        rt = RiskType(
            name='property',
            label='Property',
            description='Real Estate',
        )
        db.session.add(rt)
        rt.fields.extend([
            RiskField(
                type_name='first_name',
                label="First Name",
            ),
            RiskField(
                type_name='address',
                label="Address",
            ),
            RiskField(
                type_name='insured value',
                label="Insured Value",
            ),
        ])
        rt = RiskType(
            name='hole-in-one',
            label='Hole in One',
            description='Hole-in-One contest',
        )
        rt.fields.extend([
            RiskField(
                type_name='salutation',
                label="Salutation",
            ),
            RiskField(
                type_name='points',
                label="Points",
            ),
            RiskField(
                type_name='event_name',
                label="Event Name",
            ),
            RiskField(
                type_name='date',
                label="Event Date",
            ),
            RiskField(
                type_name='probability',
                label="Probability",
            ),
            RiskField(
                type_name='reward value',
                label="Reward Value",
            ),
        ])
        db.session.add(rt)
        db.session.commit()
