from fastapi import APIRouter, HTTPException
from typing import List
from app.models import Category
from app.schemas import CategoryUpdate
from app.crud import get_categories, update_category, delete_category

router = APIRouter()

@router.get("/categories", response_model=List[Category])
def list_categories():
    """Return all categories."""
    return get_categories()


@router.put("/categories/{category_id}", response_model=Category)
def update_existing_category(category_id: int, category: CategoryUpdate):
    """Update fields on an existing category."""
    updated = update_category(category_id, category)
    if not updated:
        raise HTTPException(status_code=404, detail="Category not found")
    return updated


@router.delete("/categories/{category_id}", status_code=204)
def delete_existing_category(category_id: int):
    """Delete a category by id."""
    if not delete_category(category_id):
        raise HTTPException(status_code=404, detail="Category not found")
    return {}