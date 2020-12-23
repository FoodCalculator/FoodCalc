from flask import Flask, render_template, request, redirect, session
from cs50 import SQL


# Configure app
app = Flask(__name__)

# Ensure app realoads on templates changes
app.config["TEMPLATES_AUTO_RELOAD"] = True

db = SQL("sqlite:///foodcalc.db")

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET"])
def index():
    return render_template("foods.html")


@app.route("/add", methods=["POST", "GET"])
def add():

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
        sod = float(request.form.get("sod"))
        pot = float(request.form.get("pot"))

        if brand == "":
            brand = None
        
        db.execute("INSERT INTO foods (brand, name, desc, amount, amount_type, total_servs, cal, fat, carb, fiber, prot, sugar, sodium, potassium) " +
            "VALUES(:brand, :name, :desc, :amount, :amount_type, :total_servs, :cal, :fat, :carb, :fiber, :prot, :sugar, :sodium, :potassium)",
            brand=brand, name=name, desc= desc, amount=amount, amount_type=amount_type, total_servs=total_servs, cal=cal, fat=fat, carb=carb, fiber=fib, prot=prot, sugar=sugar, sodium=sod, potassium=pot)

        return redirect("/")
    else:
        return render_template("add.html")


@app.route("/search", methods=["POST", "GET"])
def search():
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
            rows = db.execute("SELECT * FROM foods WHERE foods.name LIKE :name ORDER BY foods.clicks DESC", name=name)
        elif brand and not name:
            rows = db.execute("SELECT * FROM foods WHERE foods.brand LIKE :brand ORDER BY foods.clicks DESC", brand=brand)
        elif name and brand:
            rows = db.execute("SELECT * FROM foods WHERE foods.name LIKE :name AND foods.brand LIKE :brand ORDER BY foods.clicks DESC", name=name, brand=brand)
        else:
            rows = []

        if len(rows) == 0:
            message = "No results found"
        else:
            message = "Results"

        return render_template("search.html", rows=rows, top_message=message)

    else:
        # later order by advertised (since the user has not searched a food yet)
        rows = db.execute("SELECT * FROM foods ORDER BY foods.clicks DESC LIMIT 100")

        return render_template("search.html", rows=rows, top_message="Top Foods")


@app.route("/calc", methods=["POST"])
def calc():

    id = int(request.form.get("id"))
    multiplier = float(request.form.get("multiplier"))

    # fetch the food to be calculated
    rows = db.execute("SELECT * FROM foods WHERE foods.id = :id LIMIT 1", id=id)

    # update the clicks the food has (usage popularity)
    db.execute("UPDATE foods SET clicks = clicks + 1 WHERE foods.id = :id", id=id)

    return render_template("calc.html", row=rows[0], multiplier=multiplier)


@app.route("/edit", methods=["POST"])
def edit():

    post_type = str(request.form.get("post_type")).lower()

    id = int(request.form.get("id"))

    if post_type == "load":

        rows = db.execute("SELECT * FROM foods WHERE foods.id = :id LIMIT 1", id=id)

        # update the clicks the food has (usage popularity)
        db.execute("UPDATE foods SET clicks = clicks + 1 WHERE foods.id = :id", id=id)

        return render_template("edit.html", row=rows[0])

    elif post_type == "edit":

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
        sod = float(request.form.get("sod"))
        pot = float(request.form.get("pot"))

        if brand == "":
            brand = None

        rows = db.execute("UPDATE foods SET brand = :brand, name = :name, desc = :desc, amount = :amount, amount_type = :amount_type, total_servs = :total_servs, cal = :cal, fat = :fat, carb = :carb, fiber = :fiber, prot = :prot, sugar = :sugar, sodium = :sodium, potassium = :potassium " +
            "WHERE foods.id = :id",
            brand=brand, name=name, desc=desc, amount=amount, amount_type=amount_type, total_servs=total_servs, cal=cal, fat=fat, carb=carb, fiber=fib, prot=prot, sugar=sugar, sodium=sod, potassium=pot,
            id=id)

        return redirect("/search")

if __name__ == '__main__':
    app.run()