from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///expenses.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)


categories = ["Food", "Travel", "Shopping", "Other"]


@app.route("/")
def index():
    selected_category = request.args.get("category")

    if selected_category:
        expenses = Expense.query.filter_by(category=selected_category).all()
    else:
        expenses = Expense.query.all()

    total = sum(expense.amount for expense in expenses)

    return render_template(
        "index.html",
        expenses=expenses,
        total=total,
        categories=categories,
        selected_category=selected_category
    )


@app.route("/add", methods=["POST"])
def add_expense():
    title = request.form["title"]
    amount = float(request.form["amount"])
    category = request.form["category"]

    expense = Expense(
        title=title,
        amount=amount,
        category=category
    )

    db.session.add(expense)
    db.session.commit()

    return redirect(url_for("index"))


@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_expense(id):
    expense = Expense.query.get_or_404(id)

    if request.method == "POST":
        expense.title = request.form["title"]
        expense.amount = float(request.form["amount"])
        expense.category = request.form["category"]

        db.session.commit()

        return redirect(url_for("index"))

    return render_template(
        "edit.html",
        expense=expense,
        categories=categories
    )


@app.route("/delete/<int:id>", methods=["POST"])
def delete_expense(id):
    expense = Expense.query.get_or_404(id)

    db.session.delete(expense)
    db.session.commit()

    return redirect(url_for("index"))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)
# Jenkins CI test
# Automatic Jenkins build test
