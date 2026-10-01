from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import MenuItem, Restaurant
from app.schemas import MenuItemCreate, MenuItemOut

router = APIRouter(prefix="/api/menu", tags=["Menu"])

@router.post("", response_model=MenuItemOut, status_code=201)
def create_menu_item(data: MenuItemCreate, db: Session = Depends(get_db)):
    if not db.get(Restaurant, data.restaurant_id):
        raise HTTPException(status_code=404, detail="Restaurant not found")
    item = MenuItem(**data.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

@router.get("/restaurant/{restaurant_id}", response_model=list[MenuItemOut])
def list_menu(restaurant_id: int, db: Session = Depends(get_db)):
    if not db.get(Restaurant, restaurant_id):
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return db.query(MenuItem).filter(MenuItem.restaurant_id == restaurant_id).order_by(MenuItem.id).all()

@router.get("/{item_id}", response_model=MenuItemOut)
def get_menu_item(item_id: int, db: Session = Depends(get_db)):
    item = db.get(MenuItem, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Menu item not found")
    return item

@router.put("/{item_id}", response_model=MenuItemOut)
def update_menu_item(item_id: int, data: MenuItemCreate, db: Session = Depends(get_db)):
    item = db.get(MenuItem, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Menu item not found")
    for key, value in data.model_dump().items():
        setattr(item, key, value)
    db.commit()
    db.refresh(item)
    return item

@router.delete("/{item_id}", status_code=204)
def delete_menu_item(item_id: int, db: Session = Depends(get_db)):
    item = db.get(MenuItem, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Menu item not found")
    db.delete(item)
    db.commit()
