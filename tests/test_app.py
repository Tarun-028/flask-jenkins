import pytest

from app import app, db, Expense


@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

    with app.app_context():
        db.drop_all()
        db.create_all()

    with app.test_client() as client:
        yield client

    with app.app_context():
        db.session.remove()
        db.drop_all()


def test_homepage_loads(client):
    response = client.get("/")

    assert response.status_code == 200
    assert b"Expense Tracker" in response.data


def test_adding_expense(client):
    response = client.post(
        "/add",
        data={
            "title": "Lunch",
            "amount": "150",
            "category": "Food"
        },
        follow_redirects=True
    )

    assert response.status_code == 200
    assert b"Lunch" in response.data
    assert b"150.00" in response.data

    with app.app_context():
        expense = Expense.query.first()

        assert expense is not None
        assert expense.title == "Lunch"
        assert expense.amount == 150
        assert expense.category == "Food"


def test_deleting_expense(client):
    with app.app_context():
        expense = Expense(
            title="Bus Ticket",
            amount=50,
            category="Travel"
        )

        db.session.add(expense)
        db.session.commit()

        expense_id = expense.id

    response = client.post(
        f"/delete/{expense_id}",
        follow_redirects=True
    )

    assert response.status_code == 200
    assert b"Bus Ticket" not in response.data

    with app.app_context():
        assert db.session.get(Expense, expense_id) is None
