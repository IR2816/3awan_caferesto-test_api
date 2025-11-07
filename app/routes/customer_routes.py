from fastapi import APIRouter, HTTPException
from typing import List
from app.schemas import CustomerCreate, CustomerRead, CustomerUpdate
from app.crud import create_customer, get_customers, get_customer, update_customer, delete_customer
from fastapi import Depends
from app.utils.jwt import get_current_user

router = APIRouter()

@router.post("/customers", response_model=CustomerRead, status_code=201)
def create_new_customer(customer: CustomerCreate, current_user=Depends(get_current_user)):
    """Create a new customer."""
    return create_customer(customer)

@router.get("/customers", response_model=List[CustomerRead])
def list_customers():
    return get_customers()

@router.get("/customers/{customer_id}", response_model=CustomerRead)
def read_customer(customer_id: int):
    c = get_customer(customer_id)
    if not c:
        raise HTTPException(status_code=404, detail="Customer not found")
    return c

@router.put("/customers/{customer_id}", response_model=CustomerRead)
def update_existing_customer(customer_id: int, customer: CustomerUpdate, current_user=Depends(get_current_user)):
    """Update fields on an existing customer."""
    updated = update_customer(customer_id, customer)
    if not updated:
        raise HTTPException(status_code=404, detail="Customer not found")
    return updated

@router.delete("/customers/{customer_id}", status_code=204)
def delete_existing_customer(customer_id: int, current_user=Depends(get_current_user)):
    """Delete a customer by id."""
    if not delete_customer(customer_id):
        raise HTTPException(status_code=404, detail="Customer not found")
    return {}