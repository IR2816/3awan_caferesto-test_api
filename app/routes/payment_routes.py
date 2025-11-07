from fastapi import APIRouter, HTTPException
from app.schemas import PaymentCreate, PaymentRead, PaymentUpdate
from app.crud import create_payment, get_payment, update_payment, delete_payment
from fastapi import Depends
from app.utils.jwt import get_current_user

router = APIRouter()

@router.post("/payments", response_model=PaymentRead, status_code=201)
def create_new_payment(payment: PaymentCreate, current_user=Depends(get_current_user)):
    """Create a payment for an order."""
    try:
        return create_payment(payment)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/payments/{payment_id}", response_model=PaymentRead)
def read_payment(payment_id: int):
    """Get a single payment by id."""
    payment = get_payment(payment_id)
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment


@router.put("/payments/{payment_id}", response_model=PaymentRead)
def update_existing_payment(payment_id: int, payment: PaymentUpdate, current_user=Depends(get_current_user)):
    """Update fields on an existing payment."""
    updated = update_payment(payment_id, payment)
    if not updated:
        raise HTTPException(status_code=404, detail="Payment not found")
    return updated


@router.delete("/payments/{payment_id}", status_code=204)
def delete_existing_payment(payment_id: int, current_user=Depends(get_current_user)):
    """Delete a payment by id."""
    if not delete_payment(payment_id):
        raise HTTPException(status_code=404, detail="Payment not found")
    return {}