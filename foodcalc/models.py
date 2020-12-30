"""The models and the database instance."""

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Food(db.Model):
    """A food."""

    __tablename__ = "foods"  # Compatibility with old code.
    id = db.Column(db.Integer, primary_key=True)
    # Should probably be a string, but I am keeping it for compatibility.
    brand = db.Column(db.Text)  # Same applies to most of these text fields.
    name = db.Column(db.Text)
    desc = db.Column(db.Text)
    total_servs = db.Column(db.Text)
    amount = db.Column(db.Integer)
    amount_type = db.Column(db.Text)
    cal = db.Column(db.Integer)
    fat = db.Column(db.Integer)
    carb = db.Column(db.Integer)
    fiber = db.Column(db.Integer)
    prot = db.Column(db.Integer)
    sugar = db.Column(db.Integer)
    sodium = db.Column(db.Integer)
    cholesterol = db.Column(db.Integer)
    potassium = db.Column(db.Integer)
    clicks = db.Column(db.Integer)
    date = db.Column(db.Integer)
