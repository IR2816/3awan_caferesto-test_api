"""Local dev smoke-test runner.

This script provides a quick way to verify basic CRUD flows with an in-memory SQLite database.
Useful for checking API behavior during development.

Usage (PowerShell):
    & ./venv/Scripts/python.exe -m dev.smoke_test
"""
from sqlmodel import create_engine, SQLModel, Session
from fastapi.testclient import TestClient

import app.database as database
import app.crud as crud
from app import main
# Import all models to ensure they are registered with SQLModel
from app.models import (
    Category,
    Menu,
    Customer,
    MenuAddon,
    Order
)


def setup_test_db():
    """Set up a fresh in-memory database for testing."""
    # Create an SQLite in-memory database engine
    engine = create_engine(
        "sqlite:///:memory:",
        echo=True,  # Enable echo to see SQL operations
        connect_args={"check_same_thread": False}
    )

    # Override the production engine in both database and crud modules
    database.engine = engine
    crud.engine = engine

    # Create all tables directly
    try:
        SQLModel.metadata.create_all(engine)
        print("Tables created successfully")
    except Exception as e:
        print(f"Error creating tables: {e}")
        raise

    return engine


def seed_test_data(engine):
    """Seed minimal test data."""
    with Session(engine) as session:
        # Create category
        cat = Category(name="Beverages")
        session.add(cat)
        session.commit()

        # Create menu item
        menu = Menu(
            name="Espresso",
            price=2.50,
            category_id=cat.id,
            description="Strong coffee",
        )
        session.add(menu)
        session.commit()

        # Create addon
        addon = MenuAddon(
            menu_id=menu.id,
            name="Extra Shot",
            price=0.50
        )
        session.add(addon)
        session.commit()

        # Create customer
        customer = Customer(
            name="Dev User",
            phone="+621234567"
        )
        session.add(customer)
        session.commit()

        return {
            "category_id": cat.id,
            "menu_id": menu.id,
            "addon_id": addon.id,
            "customer_id": customer.id
        }


def test_create_customer(client):
    """Test customer creation endpoint."""
    print("\n-> Testing /api/customers creation")
    r = client.post(
        "/api/customers",
        json={
            "name": "Alice Test",
            "phone": "+628111222333"
        }
    )
    print(f"Status: {r.status_code}")
    data = r.json()
    print(f"Response: {data}")
    assert r.status_code == 201
    assert data["name"] == "Alice Test"
    return data["id"]


def test_create_order(client, customer_id, menu_id, addon_id):
    """Test order creation endpoint."""
    print("\n-> Testing /api/orders creation")
    payload = {
        "customer_id": customer_id,
        "payment_method": "cash",
        "items": [
            {
                "menu_id": menu_id,
                "quantity": 2,
                "addon_ids": [addon_id]
            }
        ]
    }
    r = client.post("/api/orders", json=payload)
    print(f"Status: {r.status_code}")
    data = r.json()
    print(f"Response: {data}")
    assert r.status_code == 201
    # Order total should be: (menu price + addon price) * quantity
    # (2.50 + 0.50) * 2 = 6.00
    assert float(data["total"]) == 6.00
    return data["id"]


def run():
    """Run the smoke test suite."""
    print("\nStarting smoke tests...\n")

    # Set up test database
    engine = setup_test_db()
    print("✓ Test database initialized")

    # Seed initial data
    ids = seed_test_data(engine)
    print("✓ Test data seeded")

    # Create test client
    client = TestClient(main.app)

    # Run tests
    try:
        # Test customer creation
        new_customer_id = test_create_customer(client)

        # Test order creation (using the newly created customer)
        order_id = test_create_order(
            client,
            customer_id=new_customer_id,
            menu_id=ids["menu_id"],
            addon_id=ids["addon_id"]
        )

        print("\n✓ All smoke tests passed!")

    except Exception as e:
        print(f"\n✗ Tests failed: {str(e)}")
        raise


if __name__ == "__main__":
    run()