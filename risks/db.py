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

#
#
#class EnumValues(db.Model):
#    id = db.Column(db.Integer, primary_key=True)
#    field_name = db.Column(db.ForeignKey(RiskFieldType.name))
#    value = db.Column(db.Text)  # JSON-ified
#
#
#class RiskType(db.Model):
#    name = db.Column(db.Text, primary_key=True)
#    desription = db.Column(db.Text)
#    fields = db.Column(db.Text)  # JSON-ified
#
#
#class Risk(db.Model):
#    id = db.Column(db.Integer, primary_key=True)
#    type = db.Column(db.Text, db.ForeignKey(RiskType.name))
