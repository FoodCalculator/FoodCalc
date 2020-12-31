"""The main blueprint."""

from flask import Blueprint, render_template, request, redirect, abort, flash, url_for
from flask_security import login_required, current_user

from foodcalc.models import db, Food


bp = Blueprint('main', __name__)


@bp.route("/", methods=["GET"])
def index():
    """Show the home page."""
    return render_template("foods.html")


@bp.route("/add", methods=["POST", "GET"])
@login_required
def add():
    """Add a food."""
    if request.method == "POST":

        brand = str(request.form.get("brand")).title()
        name = str(request.form.get("name")).title()
        desc = str(request.form.get("desc")).title()
        amount = float(request.form.get("amount"))
        amount_type = str(request.form.get("amount_type")).lower()
        total_servs = float(request.form.get("total_servs"))
        cal = float(request.form.get("cal"))
        fat = float(request.form.get("fat"))
        carb = float(request.form.get("carb"))
        fib = float(request.form.get("fib"))
        prot = float(request.form.get("prot"))
        sugar = float(request.form.get("sugar"))
        chol = float(request.form.get("chol"))
        sod = float(request.form.get("sod"))
        pot = float(request.form.get("pot"))

        if brand == "":
            brand = None

        newfood = Food(brand=brand, name=name, desc=desc, amount=amount,
                       amount_type=amount_type, total_servs=total_servs,
                       cal=cal, fat=fat, carb=carb, fiber=fib, prot=prot,
                       sugar=sugar, sodium=sod, potassium=pot,
                       user_id=current_user.id, active=False, cholesterol=chol)
        db.session.add(newfood)
        db.session.commit()

        return redirect("/")

    return render_template("add.html")


@bp.route("/search", methods=["POST", "GET"])
def search():
    """Search for a food."""
    # TODO
    # -  Search foods
    # -  Calculate foods in the search bar when user clicks "calculate" and
    #    take them to the calc page with the numbers calculated
    # -  Edit foods in search when user clicks edit

    if request.method == "POST":

        brand = str(request.form.get("brand").title())
        name = str(request.form.get("name").title())

        if brand == "":
            brand = None
        if name == "":
            name = None

        if name and not brand:
            rows = Food.query.filter(Food.name.like(name)).order_by(
                Food.clicks).filter(Food.active is True).all()
        elif brand and not name:
            rows = Food.query.filter(Food.brand.like(brand)).order_by(
                Food.clicks).filter(Food.active is True).all()
        elif name and brand:
            rows = Food.query.filter(
                Food.name.like(name) and Food.brand.like(brand)
                ).order_by(Food.clicks).filter(
                    Food.active is True).all()
        else:
            rows = []

        if len(rows) == 0:
            message = "No results found"
        else:
            message = "Results"

        return render_template("search.html", rows=rows, top_message=message)

    # later order by advertised
    # (since the user has not searched a food yet)
    rows = Food.query.order_by(Food.clicks).limit(100).all()

    return render_template("search.html", rows=rows,
                           top_message="Top Foods")


@bp.route("/calc", methods=["POST"])
def calc():
    """Calculate a food multiplier."""
    food_id = int(request.form.get("id"))
    multiplier = float(request.form.get("multiplier"))

    # fetch the food to be calculated
    food = Food.query.filter(Food.id == food_id).first()

    # update the clicks the food has (usage popularity)
    if food.clicks is None:
        food.clicks = 1
    else:
        food.clicks += 1

    db.session.add(food)
    db.session.commit()

    return render_template("calc.html", row=food, multiplier=multiplier)


@bp.route("/edit", methods=["POST"])
@login_required
def edit():
    """Edit a food."""
    post_type = str(request.form.get("post_type")).lower()

    food_id = int(request.form.get("id"))

    if post_type == "load":
        food = Food.query.filter(Food.id == food_id).first()

        if food.user_id != current_user.id:
            flash('You can only edit foods posted by you.')
            return redirect(url_for('main.search'))

        # update the clicks the food has (usage popularity)
        if food.clicks is None:
            food.clicks = 1
        else:
            food.clicks += 1
        db.session.add(food)
        db.session.commit()

        return render_template("edit.html", row=food)

    if post_type == "edit":

        brand = str(request.form.get("brand")).title()
        name = str(request.form.get("name")).title()
        desc = str(request.form.get("desc")).title()
        amount = float(request.form.get("amount"))
        amount_type = str(request.form.get("amount_type")).lower()
        total_servs = float(request.form.get("total_servs"))
        cal = float(request.form.get("cal"))
        fat = float(request.form.get("fat"))
        carb = float(request.form.get("carb"))
        fib = float(request.form.get("fib"))
        prot = float(request.form.get("prot"))
        sugar = float(request.form.get("sugar"))
        chol = float(request.form.get("chol"))
        sod = float(request.form.get("sod"))
        pot = float(request.form.get("pot"))

        if brand == "":
            brand = None

        food = Food.query.filter(Food.id == food_id).first()

        if food.user_id != current_user.id:
            flash('You can only edit foods posted by you.')
            return redirect(url_for('main.search'))

        food.brand = brand
        food.name = name
        food.desc = desc
        food.amount = amount
        food.amount_type = amount_type
        food.total_servs = total_servs
        food.cal = cal
        food.fat = fat
        food.carb = carb
        food.fiber = fib
        food.prot = prot
        food.sugar = sugar
        food.cholesterol = chol
        food.sodium = sod
        food.potassium = pot

        db.session.add(food)
        db.session.commit()

        return redirect("/search")
    return abort(400)
