from fastapi import FastAPI, HTTPException
from typing import List, Optional
from .database import init_db
from fastapi import FastAPI, Depends
import app.database as database
from sqlmodel import Session
from fastapi.middleware.cors import CORSMiddleware
# explicit imports instead of wildcard to make dependencies clear
from .models import Category, Menu, Order, OrderItem
from .schemas import (
    MenuCreate,
    MenuUpdate,
    OrderCreate,
    CustomerCreate,
    CustomerRead,
    AddonCreate,
    AddonRead,
    PaymentCreate,
    PaymentRead,
)
from .crud import (
    get_categories,
    get_menus,
    get_menu,
    create_menu,
    update_menu,
    delete_menu,
    create_order,
    create_customer,
    get_customers,
    get_customer,
    create_addon,
    get_addons_by_menu,
    create_payment,
)

app = FastAPI(title="3awan Cafe & Resto API")

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    # Use a regex so any localhost/127.0.0.1 origin (any port) is allowed.
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_session():
    eng = database.engine
    if eng is None:
        raise RuntimeError("Database engine is not configured. Set DATABASE_URL or call database.set_engine().")
    with Session(eng) as session:
        yield session

# @app.on_event("startup")
# def on_startup():
#     init_db()

# CATEGORY
@app.get("/api/categories", response_model=List[Category])
def list_categories():
    """Return all categories."""
    return get_categories()

# MENU
@app.get("/api/menus", response_model=List[Menu])
def list_menus(category_id: Optional[int] = None):
    """List menus, optionally filtered by category_id."""
    return get_menus(category_id)

@app.get("/api/menus/{menu_id}", response_model=Menu)
def read_menu(menu_id: int):
    """Get a single menu by id."""
    menu = get_menu(menu_id)
    if not menu:
        raise HTTPException(status_code=404, detail="Menu not found")
    return menu

@app.post("/api/menus", response_model=Menu, status_code=201)
def create_new_menu(menu: MenuCreate):
    """Create a new menu item from validated input."""
    return create_menu(menu)

@app.put("/api/menus/{menu_id}", response_model=Menu)
def update_existing_menu(menu_id: int, menu: MenuUpdate):
    """Update fields on an existing menu item."""
    updated = update_menu(menu_id, menu)
    if not updated:
        raise HTTPException(status_code=404, detail="Menu not found")
    return updated

@app.delete("/api/menus/{menu_id}", status_code=204)
def delete_existing_menu(menu_id: int):
    """Delete a menu by id."""
    if not delete_menu(menu_id):
        raise HTTPException(status_code=404, detail="Menu not found")
    return {}

# ADDONS
@app.get("/api/menus/{menu_id}/addons", response_model=List[AddonRead])
def list_addons(menu_id: int):
    """List addons for a menu."""
    return get_addons_by_menu(menu_id)

@app.post("/api/menus/{menu_id}/addons", response_model=AddonRead, status_code=201)
def create_menu_addon(menu_id: int, addon: AddonCreate):
    """Create an addon for a menu."""
    try:
        return create_addon(menu_id, addon)
    except ValueError:
        raise HTTPException(status_code=404, detail="Menu not found")

# CUSTOMERS
@app.post("/api/customers", response_model=CustomerRead, status_code=201)
def create_new_customer(customer: CustomerCreate):
    """Create a new customer."""
    return create_customer(customer)

@app.get("/api/customers", response_model=List[CustomerRead])
def list_customers():
    return get_customers()

@app.get("/api/customers/{customer_id}", response_model=CustomerRead)
def read_customer(customer_id: int):
    c = get_customer(customer_id)
    if not c:
        raise HTTPException(status_code=404, detail="Customer not found")
    return c

# PAYMENTS
@app.post("/api/payments", response_model=PaymentRead, status_code=201)
def create_new_payment(payment: PaymentCreate):
    """Create a payment for an order."""
    try:
        return create_payment(payment)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# ORDER
@app.post("/api/orders", response_model=Order, status_code=201)
def create_new_order(order: OrderCreate):
    """Create a new order with items (validated)."""
    try:
        return create_order(order)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
