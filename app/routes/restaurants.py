from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Restaurant
from app.schemas import RestaurantCreate, RestaurantOut

router = APIRouter(prefix="/api/restaurants", tags=["Restaurants"])

@router.post("", response_model=RestaurantOut, status_code=201)
def create_restaurant(data: RestaurantCreate, db: Session = Depends(get_db)):
    restaurant = Restaurant(**data.model_dump())
    db.add(restaurant)
    db.commit()
    db.refresh(restaurant)
    return restaurant

@router.get("", response_model=list[RestaurantOut])
def list_restaurants(db: Session = Depends(get_db)):
    return db.query(Restaurant).order_by(Restaurant.id).all()

@router.get("/{restaurant_id}", response_model=RestaurantOut)
def get_restaurant(restaurant_id: int, db: Session = Depends(get_db)):
    restaurant = db.get(Restaurant, restaurant_id)
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return restaurant

@router.put("/{restaurant_id}", response_model=RestaurantOut)
def update_restaurant(restaurant_id: int, data: RestaurantCreate, db: Session = Depends(get_db)):
    restaurant = db.get(Restaurant, restaurant_id)
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    for key, value in data.model_dump().items():
        setattr(restaurant, key, value)
    db.commit()
    db.refresh(restaurant)
    return restaurant

@router.delete("/{restaurant_id}", status_code=204)
def delete_restaurant(restaurant_id: int, db: Session = Depends(get_db)):
    restaurant = db.get(Restaurant, restaurant_id)
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    db.delete(restaurant)
    db.commit()
