from .database import engine, init_db
from .models import SQLModel, Category, Menu, Customer, MenuAddon
from sqlmodel import Session


def seed():
    """Create some initial categories, menus, customers and addons for development/testing."""
    init_db()
    with Session(engine) as session:
        # check existing
        existing = session.exec("SELECT 1 FROM categories LIMIT 1").first()
        if existing:
            return

        cat1 = Category(name="Coffee")
        cat2 = Category(name="Snack")
        session.add(cat1)
        session.add(cat2)
        session.commit()

        menu1 = Menu(name="Espresso", price=2.5, category_id=cat1.id)
        menu2 = Menu(name="Cappuccino", price=3.0, category_id=cat1.id)
        menu3 = Menu(name="Banana Cake", price=4.0, category_id=cat2.id)
        session.add_all([menu1, menu2, menu3])
        session.commit()

        # sample customers
        cust1 = Customer(name="John Doe", phone="+628123456789")
        cust2 = Customer(name="Jane Smith", phone="+628987654321")
        session.add_all([cust1, cust2])
        session.commit()

        # sample addons
        addon1 = MenuAddon(menu_id=menu1.id, name="Extra Shot", price=0.5)
        addon2 = MenuAddon(menu_id=menu2.id, name="Soy Milk", price=0.3)
        session.add_all([addon1, addon2])
        session.commit()


if __name__ == "__main__":
    seed()
