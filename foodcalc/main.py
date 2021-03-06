"""The main blueprint."""

from flask import Blueprint, render_template, request, redirect, abort, flash, url_for
from flask_security import login_required, current_user, user_authenticated

from foodcalc.models import db, Food


bp = Blueprint('main', __name__)


@bp.route("/", methods=["GET"])
def index():
    """Show the home page."""
    # later order by advertised
    # (since the user has not searched a food yet)
    if current_user.is_authenticated:
        message = "Your top foods"
        rows = Food.query.order_by(Food.clicks).filter(Food.user_id == current_user.id).limit(100).all()
        
        # if the user hasn't added any foods
        if len(rows) == 0:
            message = "You don't seem to have any foods yet!"
    else:
        rows = Food.query.order_by(Food.clicks).limit(100).all()
        message = "Top foods"

    return render_template("foods.html", rows=rows, top_message=message)


@bp.route("/add", methods=["POST", "GET"])
@login_required
def add():
    """Add a food."""
    if request.method == "POST":
    
        brand = str(request.form.get("brand")).title()
        name = str(request.form.get("name")).title()
        desc = str(request.form.get("desc")).title()
        if len(request.form.get("amount")):
            amount = float(request.form.get("amount"))
        else:
            amount = 0
        if len(request.form.get("amount_type")):
            amount_type = str(request.form.get("amount_type")).lower()
        else:
            amount_type = 0
        if len(request.form.get("total_servs")):
            total_servs = float(request.form.get("total_servs"))
        else:
            total_servs = 0
        if len(request.form.get("cal")):
            cal = float(request.form.get("cal"))
        else:
            cal = 0
        if len(request.form.get("fat")): 
            fat = float(request.form.get("fat"))
        else:
            fat = 0
        if len(request.form.get("carb")):
            carb = float(request.form.get("carb"))
        else:
            carb = 0
        if len(request.form.get("fib")):
            fib = float(request.form.get("fib"))
        else:
            fib = 0
        if len(request.form.get("prot")):
            prot = float(request.form.get("prot"))
        else:
            prot = 0
        if len(request.form.get("sugar")):
            sugar = float(request.form.get("sugar"))
        else:
            sugar = 0
        if len(request.form.get("chol")):
            chol = float(request.form.get("chol"))
        else:
            chol = 0
        if len(request.form.get("sod")):
            sod = float(request.form.get("sod"))
        else:
            sod = 0
        if len(request.form.get("pot")):
            pot = float(request.form.get("pot"))
        else:
            pot = 0

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

    brands = Food.query.distinct(Food.brand)

    return render_template("add.html", brands=brands)


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

        return render_template("searched.html", rows=rows, top_message=message)

    # TODO later have advertised foods shown before the user searches
    return render_template("search.html")


@bp.route("/calc", methods=["POST"])
def calc():
    """Calculate a food multiplier."""

    food_id = int(request.form.get("id"))
    multiplier = 0

    # fetch the food to be calculated
    food = Food.query.filter(Food.id == food_id).first()

    # update the clicks the food has (usage popularity)
    if food.clicks is None:
        food.clicks = 1
    else:
        food.clicks += 1

    db.session.add(food)
    db.session.commit()

    # check if the user is in calc.html or coming from searched.html
    # (which will affect the input received)
    post_type = str(request.form.get("post_type"))
    if post_type == "desired":

        # get the basic info from the user of what they are wanting
        value_type = str(request.form.get("value_type"))
        desired_value = float(request.form.get("desired_value"))
        cur_value = 0.0

        if value_type == "amount":
            cur_value = food.amount
        elif value_type == "cal":
            cur_value = food.cal
        elif value_type == "fat":
            cur_value = food.fat
        elif value_type == "carb":
            cur_value = food.carb
        elif value_type == "fib":
            cur_value = food.fiber
        elif value_type == "prot":
            cur_value = food.prot
        elif value_type == "sug":
            cur_value = food.sugar
        elif value_type == "sod":
            cur_value = food.sodium
        elif value_type == "pot":
            cur_value = food.potassium
        elif value_type == "chol":
            cur_value = food.cholesterol
        else:
            multiplier = 1

        try:
            multiplier = desired_value / cur_value
        except ZeroDivisionError:
            multiplier = desired_value
            
            flash(f"Silly! You can't get {desired_value} from 0!")

    # check if the user just using the multiplier bottom left button
    elif post_type == "calc":
        multiplier = float(request.form.get("multiplier"))
    else: #post_type == "load":
        multiplier = 1

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
        if len(request.form.get("amount")):
            amount = float(request.form.get("amount"))
        else:
            amount = 0
        if len(request.form.get("amount_type")):
            amount_type = str(request.form.get("amount_type")).lower()
        else:
            amount_type = 0
        if len(request.form.get("total_servs")):
            total_servs = float(request.form.get("total_servs"))
        else:
            total_servs = 0
        if len(request.form.get("cal")):
            cal = float(request.form.get("cal"))
        else:
            cal = 0
        if len(request.form.get("fat")): 
            fat = float(request.form.get("fat"))
        else:
            fat = 0
        if len(request.form.get("carb")):
            carb = float(request.form.get("carb"))
        else:
            carb = 0
        if len(request.form.get("fib")):
            fib = float(request.form.get("fib"))
        else:
            fib = 0
        if len(request.form.get("prot")):
            prot = float(request.form.get("prot"))
        else:
            prot = 0
        if len(request.form.get("sugar")):
            sugar = float(request.form.get("sugar"))
        else:
            sugar = 0
        if len(request.form.get("chol")):
            chol = float(request.form.get("chol"))
        else:
            chol = 0
        if len(request.form.get("sod")):
            sod = float(request.form.get("sod"))
        else:
            sod = 0
        if len(request.form.get("pot")):
            pot = float(request.form.get("pot"))
        else:
            pot = 0

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

        return redirect("/")
    return abort(400)
