from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from sqlmodel import Session
from app.database import get_session
from app.models import Menu
from app.schemas import MenuCreate, MenuUpdate
from app.crud import get_menus, get_menu, create_menu, update_menu, delete_menu
from fastapi import Depends
from app.utils.jwt import get_current_user

router = APIRouter()

@router.get("/menus", response_model=List[Menu])
def list_menus(category_id: Optional[int] = None):
    """List menus, optionally filtered by category_id."""
    return get_menus(category_id)

@router.get("/menus/{menu_id}", response_model=Menu)
def read_menu(menu_id: int):
    """Get a single menu by id."""
    menu = get_menu(menu_id)
    if not menu:
        raise HTTPException(status_code=404, detail="Menu not found")
    return menu

@router.post("/menus", response_model=Menu, status_code=201)
def create_new_menu(menu: MenuCreate, current_user=Depends(get_current_user)):
    """Create a new menu item from validated input."""
    return create_menu(menu)

@router.put("/menus/{menu_id}", response_model=Menu)
def update_existing_menu(menu_id: int, menu: MenuUpdate, current_user=Depends(get_current_user)):
    """Update fields on an existing menu item."""
    updated = update_menu(menu_id, menu)
    if not updated:
        raise HTTPException(status_code=404, detail="Menu not found")
    return updated

@router.delete("/menus/{menu_id}", status_code=204)
def delete_existing_menu(menu_id: int, current_user=Depends(get_current_user)):
    """Delete a menu by id."""
    if not delete_menu(menu_id):
        raise HTTPException(status_code=404, detail="Menu not found")
    return {}