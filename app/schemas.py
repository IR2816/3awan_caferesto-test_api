from typing import Optional, List
from sqlmodel import SQLModel, Field


class UserCreate(SQLModel):
    name: str
    email: str
    password: str
    role: Optional[str] = "staff"


class UserRead(SQLModel):
    id: int
    name: str
    email: str
    role: str
    status: str


class Token(SQLModel):
    access_token: str
    token_type: str


class TokenData(SQLModel):
    email: Optional[str] = None
class CategoryRead(SQLModel):
    id: Optional[int]
    name: str


class CategoryUpdate(SQLModel):
    name: Optional[str] = None


class MenuBase(SQLModel):
    name: str
    price: float
    category_id: Optional[int] = None
    image_url: Optional[str] = None
    is_available: Optional[bool] = True
    description: Optional[str] = None


class MenuCreate(MenuBase):
    pass


class MenuUpdate(SQLModel):
    name: Optional[str] = None
    price: Optional[float] = None
    category_id: Optional[int] = None
    image_url: Optional[str] = None
    is_available: Optional[bool] = None
    description: Optional[str] = None


class OrderItemCreate(SQLModel):
    menu_id: int
    quantity: int = 1
    # client may send subtotal but server will recompute; accept but ignore
    subtotal: Optional[float] = None
    # optional addon ids attached to this item
    addon_ids: Optional[List[int]] = None


class OrderCreate(SQLModel):
    customer_id: Optional[int] = None
    payment_method: Optional[str] = "cash"
    items: List[OrderItemCreate]


class OrderUpdate(SQLModel):
    customer_id: Optional[int] = None
    payment_method: Optional[str] = None
    current_status: Optional[str] = None


class CustomerCreate(SQLModel):
    name: str
    phone_number: Optional[str] = None
    email: Optional[str] = None


class CustomerRead(SQLModel):
    id: Optional[int]
    name: str
    phone_number: Optional[str] = None
    email: Optional[str] = None


class CustomerUpdate(SQLModel):
    name: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[str] = None


class AddonCreate(SQLModel):
    name: str
    price: float


class AddonRead(SQLModel):
    id: Optional[int]
    menu_id: int
    name: str
    price: float


class AddonUpdate(SQLModel):
    name: Optional[str] = None
    price: Optional[float] = None


class PaymentCreate(SQLModel):
    order_id: int
    amount: float
    method: Optional[str] = "cash"


class PaymentRead(SQLModel):
    id: Optional[int]
    order_id: int
    amount: float
    method: Optional[str]
    status: Optional[str]
    paid_at: Optional[str]


class PaymentUpdate(SQLModel):
    amount: Optional[float] = None
    method: Optional[str] = None
    payment_status: Optional[str] = None
    paid_at: Optional[str] = None


# end
