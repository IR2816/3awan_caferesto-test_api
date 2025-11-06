"""Small dev smoke-test runner for local/manual testing.

This file is intended for local development only. It uses an in-memory
SQLite database, seeds a few records and exercises a couple of endpoints
via TestClient so you can quickly verify CRUD flows from the backend
(useful while developing the Flutter frontend).

Run with PowerShell (example):

    & .\venv\Scripts\Activate.ps1
    & .\venv\Scripts\python.exe -m app.dev_test

Do NOT use this in production.
"""
from sqlmodel import create_engine, SQLModel, Session
from fastapi.testclient import TestClient

import app.database as database
import app.crud as crud
from app import main
from app.models import Category, Menu, Customer, MenuAddon


def run():
    # create a fresh in-memory engine for dev testing
    # Use a temporary file-backed SQLite DB so the TestClient (which runs
    # the app in a different thread) can see the same data. In-memory SQLite
    # does not reliably share state across threads.
    engine = create_engine("sqlite:///./dev_tmp.db", echo=False, connect_args={"check_same_thread": False})

    # override module engine so app and crud use the same engine at runtime
    database.set_engine(engine)

    # create tables (models are imported above)
    SQLModel.metadata.create_all(engine)

    # seed minimal data directly using the same engine
    with Session(engine) as session:
        c = Category(name="DevCoffee")
        session.add(c)
        session.commit()

        m = Menu(name="DevEspresso", price=2.5, category_id=c.id)
        session.add(m)
        session.commit()
        cust = Customer(name="DevUser", phone_number="+621234")
        session.add(cust)
        session.commit()

        addon = MenuAddon(menu_id=m.id, name="Extra Shot", price=0.5)
        session.add(addon)
        session.commit()

    client = TestClient(main.app)

    print("-> Creating a new customer via /api/customers")
    r = client.post("/api/customers", json={"name": "SmokeUser", "phone_number": "+62000"})
    print(r.status_code, r.json())

    print("-> Creating an order via /api/orders")
    payload = {
        "customer_id": 1,
        "payment_method": "cash",
        "items": [{"menu_id": 1, "quantity": 2, "addon_ids": [1]}],
    }
    r2 = client.post("/api/orders", json=payload)
    print(r2.status_code, r2.json())


if __name__ == "__main__":
    run()
