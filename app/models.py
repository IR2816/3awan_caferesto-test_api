from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime


class Category(SQLModel, table=True):
    __tablename__ = "categories"
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    menus: List["Menu"] = Relationship(back_populates="category")


class Menu(SQLModel, table=True):
    __tablename__ = "menus"
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    price: float
    category_id: Optional[int] = Field(default=None, foreign_key="categories.id")
    image_url: Optional[str] = None
    description: Optional[str] = None
    is_available: bool = True
    average_rating: float = 0.0
    category: Optional[Category] = Relationship(back_populates="menus")
    addons: List["MenuAddon"] = Relationship(back_populates="menu")
    reviews: List["Review"] = Relationship(back_populates="menu")


class MenuAddon(SQLModel, table=True):
    __tablename__ = "menu_addons"
    id: Optional[int] = Field(default=None, primary_key=True)
    menu_id: int = Field(foreign_key="menus.id")
    name: str
    price: float
    menu: Optional[Menu] = Relationship(back_populates="addons")


class Customer(SQLModel, table=True):
    __tablename__ = "customers"
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    phone_number: Optional[str] = None
    email: Optional[str] = None
    orders: List["Order"] = Relationship(back_populates="customer")
    carts: List["Cart"] = Relationship(back_populates="customer")
    reviews: List["Review"] = Relationship(back_populates="customer")


class User(SQLModel, table=True):
    __tablename__ = "users"
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str = Field(index=True)
    password: str
    role: str = "staff"
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Discount(SQLModel, table=True):
    __tablename__ = "discounts"
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: Optional[str] = None
    percentage: float
    valid_until: Optional[datetime] = None


class Order(SQLModel, table=True):
    __tablename__ = "orders"
    id: Optional[int] = Field(default=None, primary_key=True)
    customer_id: Optional[int] = Field(default=None, foreign_key="customers.id")
    discount_id: Optional[int] = Field(default=None, foreign_key="discounts.id")
    total_after_discount: float = 0.0
    created_at: datetime = Field(default_factory=datetime.utcnow)
    current_status: str = "pending"
    user_id: Optional[int] = Field(default=None, foreign_key="users.id")
    customer: Optional[Customer] = Relationship(back_populates="orders")
    items: List["OrderItem"] = Relationship(back_populates="order")
    payments: List["Payment"] = Relationship(back_populates="order")
    status_history: List["OrderStatusHistory"] = Relationship(back_populates="order")


class OrderItem(SQLModel, table=True):
    __tablename__ = "order_items"
    id: Optional[int] = Field(default=None, primary_key=True)
    order_id: int = Field(foreign_key="orders.id")
    menu_id: int = Field(foreign_key="menus.id")
    quantity: int = 1
    subtotal: float = 0.0
    order: Optional[Order] = Relationship(back_populates="items")


class Cart(SQLModel, table=True):
    __tablename__ = "carts"
    id: Optional[int] = Field(default=None, primary_key=True)
    customer_id: int = Field(foreign_key="customers.id")
    menu_id: int = Field(foreign_key="menus.id")
    quantity: int = 1
    created_at: datetime = Field(default_factory=datetime.utcnow)
    customer: Optional[Customer] = Relationship(back_populates="carts")


class Payment(SQLModel, table=True):
    __tablename__ = "payments"
    id: Optional[int] = Field(default=None, primary_key=True)
    order_id: int = Field(foreign_key="orders.id")
    amount: float
    payment_method: str
    payment_status: str
    paid_at: Optional[datetime] = None
    order: Optional[Order] = Relationship(back_populates="payments")


class Review(SQLModel, table=True):
    __tablename__ = "reviews"
    id: Optional[int] = Field(default=None, primary_key=True)
    customer_id: int = Field(foreign_key="customers.id")
    menu_id: int = Field(foreign_key="menus.id")
    rating: int
    comment: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    customer: Optional[Customer] = Relationship(back_populates="reviews")
    menu: Optional[Menu] = Relationship(back_populates="reviews")


class OrderStatusHistory(SQLModel, table=True):
    __tablename__ = "order_status_history"
    id: Optional[int] = Field(default=None, primary_key=True)
    order_id: int = Field(foreign_key="orders.id")
    status: str
    note: Optional[str] = None
    changed_at: datetime = Field(default_factory=datetime.utcnow)
    order: Optional[Order] = Relationship(back_populates="status_history")