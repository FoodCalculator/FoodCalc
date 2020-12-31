"""The models and the database instance."""

from flask_sqlalchemy import SQLAlchemy
from flask_security.models import fsqla_v2 as fsqla


db = SQLAlchemy()
fsqla.FsModels.set_db_info(db)


class Role(db.Model, fsqla.FsRoleMixin):
    """A role."""


class User(db.Model, fsqla.FsUserMixin):
    """A user."""

    foods = db.relationship('Food', backref='user', lazy=True)


class Food(db.Model):
    """A food."""

    __tablename__ = "foods"
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(120))
    name = db.Column(db.String(120))
    desc = db.Column(db.String(120))
    total_servs = db.Column(db.String(120))
    amount = db.Column(db.Float)
    amount_type = db.Column(db.String(120))
    cal = db.Column(db.Float)
    fat = db.Column(db.Float)
    carb = db.Column(db.Float)
    fiber = db.Column(db.Float)
    prot = db.Column(db.Float)
    sugar = db.Column(db.Float)
    sodium = db.Column(db.Float)
    potassium = db.Column(db.Float)
    clicks = db.Column(db.Float)
    date = db.Column(db.DateTime)
    active = db.Column(db.Boolean)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    cholesterol = db.Column(db.Integer)
