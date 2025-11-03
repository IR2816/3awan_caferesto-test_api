from fastapi import APIRouter, HTTPException
from typing import List
from app.schemas import AddonCreate, AddonRead, AddonUpdate
from app.crud import get_addons_by_menu, create_addon, get_addon, update_addon, delete_addon

router = APIRouter()

@router.get("/menus/{menu_id}/addons", response_model=List[AddonRead])
def list_addons(menu_id: int):
    """List addons for a menu."""
    return get_addons_by_menu(menu_id)

@router.post("/menus/{menu_id}/addons", response_model=AddonRead, status_code=201)
def create_menu_addon(menu_id: int, addon: AddonCreate):
    """Create an addon for a menu."""
    try:
        return create_addon(menu_id, addon)
    except ValueError:
        raise HTTPException(status_code=404, detail="Menu not found")


@router.get("/addons/{addon_id}", response_model=AddonRead)
def read_addon(addon_id: int):
    """Get a single addon by id."""
    addon = get_addon(addon_id)
    if not addon:
        raise HTTPException(status_code=404, detail="Addon not found")
    return addon


@router.put("/addons/{addon_id}", response_model=AddonRead)
def update_existing_addon(addon_id: int, addon: AddonUpdate):
    """Update fields on an existing addon."""
    updated = update_addon(addon_id, addon)
    if not updated:
        raise HTTPException(status_code=404, detail="Addon not found")
    return updated


@router.delete("/addons/{addon_id}", status_code=204)
def delete_existing_addon(addon_id: int):
    """Delete an addon by id."""
    if not delete_addon(addon_id):
        raise HTTPException(status_code=404, detail="Addon not found")
    return {}