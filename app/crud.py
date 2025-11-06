from typing import List, Optional

from sqlmodel import Session, select
from .models import (
    Category,
    Menu,
    Order,
    OrderItem,
    MenuAddon,
    Customer,
    Payment,
)
from .schemas import (
    MenuCreate,
    MenuUpdate,
    OrderCreate,
    OrderUpdate,
    OrderItemCreate,
    CustomerCreate,
    CustomerUpdate,
    CategoryUpdate,
    AddonCreate,
    AddonUpdate,
    PaymentCreate,
    PaymentUpdate,
)

from . import database


# CATEGORY
def get_categories() -> List[Category]:
    """Return all categories."""
    with Session(database.engine) as session:
        return session.exec(select(Category)).all()


def update_category(category_id: int, data: dict | CategoryUpdate) -> Optional[Category]:
    """Update fields on a category using values from a dict or CategoryUpdate."""
    if isinstance(data, CategoryUpdate):
        data = data.dict(exclude_unset=True)

    with Session(database.engine) as session:
        category = session.get(Category, category_id)
        if not category:
            return None
        for key, val in data.items():
            setattr(category, key, val)
        session.add(category)
        session.commit()
        session.refresh(category)
        return category


def delete_category(category_id: int) -> bool:
    """Delete a category by id. Return True if deleted, False if not found."""
    with Session(database.engine) as session:
        category = session.get(Category, category_id)
        if not category:
            return False
        session.delete(category)
        session.commit()
        return True


# MENU
def get_menus(category_id: Optional[int] = None) -> List[Menu]:
    """Return menus, optionally filtered by category_id."""
    with Session(database.engine) as session:
        query = select(Menu)
        if category_id:
            query = query.where(Menu.category_id == category_id)
        return session.exec(query).all()


def get_menu(menu_id: int) -> Optional[Menu]:
    """Get a menu by id or return None if not found."""
    with Session(database.engine) as session:
        return session.get(Menu, menu_id)


def create_menu(menu: Menu | MenuCreate) -> Menu:
    """Persist a new menu (from a Menu or MenuCreate) and return it (with id)."""
    # normalize to Menu instance
    if isinstance(menu, MenuCreate):
        menu = Menu(**menu.dict())

    with Session(database.engine) as session:
        session.add(menu)
        session.commit()
        session.refresh(menu)
        return menu


def update_menu(menu_id: int, data: dict | MenuUpdate) -> Optional[Menu]:
    """Update fields on a menu using values from a dict or MenuUpdate."""
    if isinstance(data, MenuUpdate):
        data = data.dict(exclude_unset=True)

    with Session(database.engine) as session:
        menu = session.get(Menu, menu_id)
        if not menu:
            return None
        for key, val in data.items():
            setattr(menu, key, val)
        session.add(menu)
        session.commit()
        session.refresh(menu)
        return menu


def delete_menu(menu_id: int) -> bool:
    """Delete a menu by id. Return True if deleted, False if not found."""
    with Session(database.engine) as session:
        menu = session.get(Menu, menu_id)
        if not menu:
            return False
        session.delete(menu)
        session.commit()
        return True


# ADDONS
def create_addon(menu_id: int, addon: AddonCreate) -> MenuAddon:
    """Create an addon for a menu."""
    with Session(database.engine) as session:
        menu = session.get(Menu, menu_id)
        if not menu:
            raise ValueError("Menu not found")
        ma = MenuAddon(menu_id=menu_id, name=addon.name, price=addon.price)
        session.add(ma)
        session.commit()
        session.refresh(ma)
        return ma


def get_addons_by_menu(menu_id: int) -> List[MenuAddon]:
    """List addons for a given menu."""
    with Session(database.engine) as session:
        query = select(MenuAddon).where(MenuAddon.menu_id == menu_id)
        return session.exec(query).all()


def get_addon(addon_id: int) -> Optional[MenuAddon]:
    with Session(database.engine) as session:
        return session.get(MenuAddon, addon_id)


def update_addon(addon_id: int, data: dict | AddonUpdate) -> Optional[MenuAddon]:
    """Update fields on an addon using values from a dict or AddonUpdate."""
    if isinstance(data, AddonUpdate):
        data = data.dict(exclude_unset=True)

    with Session(database.engine) as session:
        addon = session.get(MenuAddon, addon_id)
        if not addon:
            return None
        for key, val in data.items():
            setattr(addon, key, val)
        session.add(addon)
        session.commit()
        session.refresh(addon)
        return addon


def delete_addon(addon_id: int) -> bool:
    """Delete an addon by id. Return True if deleted, False if not found."""
    with Session(database.engine) as session:
        addon = session.get(MenuAddon, addon_id)
        if not addon:
            return False
        session.delete(addon)
        session.commit()
        return True


# CUSTOMERS
def create_customer(data: CustomerCreate) -> Customer:
    with Session(database.engine) as session:
        # Accept either phone or phone_number in incoming DTOs for compatibility
        phone_val = getattr(data, "phone_number", None) or getattr(data, "phone", None)
        c = Customer(name=data.name, phone_number=phone_val, email=getattr(data, "email", None))
        session.add(c)
        session.commit()
        session.refresh(c)
        return c


def get_customers() -> List[Customer]:
    with Session(database.engine) as session:
        return session.exec(select(Customer)).all()


def get_customer(customer_id: int) -> Optional[Customer]:
    with Session(database.engine) as session:
        return session.get(Customer, customer_id)


def update_customer(customer_id: int, data: dict | CustomerUpdate) -> Optional[Customer]:
    """Update fields on a customer using values from a dict or CustomerUpdate."""
    if isinstance(data, CustomerUpdate):
        data = data.dict(exclude_unset=True)

    with Session(database.engine) as session:
        customer = session.get(Customer, customer_id)
        if not customer:
            return None
        for key, val in data.items():
            setattr(customer, key, val)
        session.add(customer)
        session.commit()
        session.refresh(customer)
        return customer


def delete_customer(customer_id: int) -> bool:
    """Delete a customer by id. Return True if deleted, False if not found."""
    with Session(database.engine) as session:
        customer = session.get(Customer, customer_id)
        if not customer:
            return False
        session.delete(customer)
        session.commit()
        return True


# PAYMENTS
def create_payment(payment: PaymentCreate) -> Payment:
    with Session(database.engine) as session:
        order = session.get(Order, payment.order_id)
        if not order:
            raise ValueError("Order not found")
        p = Payment(order_id=payment.order_id, amount=payment.amount, payment_method=getattr(payment, "method", "cash"), payment_status="paid", paid_at=None)
        session.add(p)
        # optionally update order status
        order.current_status = "completed"
        session.add(order)
        session.commit()
        session.refresh(p)
        return p


def get_payment(payment_id: int) -> Optional[Payment]:
    """Get a payment by id or return None if not found."""
    with Session(database.engine) as session:
        return session.get(Payment, payment_id)


def update_payment(payment_id: int, data: dict | PaymentUpdate) -> Optional[Payment]:
    """Update fields on a payment using values from a dict or PaymentUpdate."""
    if isinstance(data, PaymentUpdate):
        data = data.dict(exclude_unset=True)

    with Session(database.engine) as session:
        payment = session.get(Payment, payment_id)
        if not payment:
            return None
        for key, val in data.items():
            setattr(payment, key, val)
        session.add(payment)
        session.commit()
        session.refresh(payment)
        return payment


def delete_payment(payment_id: int) -> bool:
    """Delete a payment by id. Return True if deleted, False if not found."""
    with Session(database.engine) as session:
        payment = session.get(Payment, payment_id)
        if not payment:
            return False
        session.delete(payment)
        session.commit()
        return True


# ORDER
def create_order(order: Order | OrderCreate, items: List[OrderItem] | None = None) -> Order:
    """Create an order and its items. Accepts an Order instance or OrderCreate DTO.

    Computes subtotals server-side and validates customer existence when provided.
    If `items` is passed separately, it's treated as the list of OrderItem instances.
    """
    # normalize order and items
    if isinstance(order, OrderCreate):
        # compute items server-side
        items_objs: List[OrderItem] = []
        with Session(database.engine) as session:
            # if customer provided ensure exists
            if order.customer_id is not None:
                cust = session.get(Customer, order.customer_id)
                if not cust:
                    raise ValueError("Customer not found")

            total = 0
            for i in order.items:
                menu = session.get(Menu, i.menu_id)
                if not menu:
                    raise ValueError(f"Menu id {i.menu_id} not found")
                qty = max(1, i.quantity)
                # base price
                subtotal = float(menu.price) * qty
                # addons
                if i.addon_ids:
                    for aid in i.addon_ids:
                        addon = session.get(MenuAddon, aid)
                        if not addon:
                            raise ValueError(f"Addon id {aid} not found")
                        subtotal += float(addon.price) * qty

                oi = OrderItem(menu_id=i.menu_id, quantity=qty, subtotal=subtotal)
                items_objs.append(oi)
                total += subtotal

        items = items_objs
        order = Order(customer_id=order.customer_id, payment_method=order.payment_method)

    if items is None:
        items = []

    with Session(database.engine) as session:
        session.add(order)
        session.commit()
        total = 0
        for item in items:
            item.order_id = order.id
            total += item.subtotal
            session.add(item)
        # optional discount handling is caller's responsibility; set total_after_discount
        order.total_after_discount = total
        session.add(order)
        session.commit()
        session.refresh(order)
        return order


def get_order(order_id: int) -> Optional[Order]:
    """Get an order by id or return None if not found."""
    with Session(database.engine) as session:
        return session.get(Order, order_id)


def update_order(order_id: int, data: dict | OrderUpdate) -> Optional[Order]:
    """Update fields on an order using values from a dict or OrderUpdate."""
    if isinstance(data, OrderUpdate):
        data = data.dict(exclude_unset=True)

    with Session(database.engine) as session:
        order = session.get(Order, order_id)
        if not order:
            return None
        for key, val in data.items():
            setattr(order, key, val)
        session.add(order)
        session.commit()
        session.refresh(order)
        return order


def delete_order(order_id: int) -> bool:
    """Delete an order by id. Return True if deleted, False if not found."""
    with Session(database.engine) as session:
        order = session.get(Order, order_id)
        if not order:
            return False
        session.delete(order)
        session.commit()
        return True
