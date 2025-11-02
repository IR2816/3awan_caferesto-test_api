from fastapi import APIRouter, HTTPException
from ..models import Order
from ..schemas import OrderCreate, OrderUpdate
from ..crud import create_order, get_order, update_order, delete_order

router = APIRouter()

@router.post("/orders", response_model=Order, status_code=201)
def create_new_order(order: OrderCreate):
    """Create a new order with items (validated)."""
    try:
        return create_order(order)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/orders/{order_id}", response_model=Order)
def read_order(order_id: int):
    """Get a single order by id."""
    order = get_order(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@router.put("/orders/{order_id}", response_model=Order)
def update_existing_order(order_id: int, order: OrderUpdate):
    """Update fields on an existing order."""
    updated = update_order(order_id, order)
    if not updated:
        raise HTTPException(status_code=404, detail="Order not found")
    return updated


@router.delete("/orders/{order_id}", status_code=204)
def delete_existing_order(order_id: int):
    """Delete an order by id."""
    if not delete_order(order_id):
        raise HTTPException(status_code=404, detail="Order not found")
    return {}