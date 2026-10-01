from datetime import datetime
from typing import List
from pydantic import BaseModel, Field, ConfigDict

class RestaurantCreate(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    address: str = Field(min_length=2, max_length=255)
    phone: str = Field(min_length=5, max_length=20)
    status: str = "OPEN"

class RestaurantOut(RestaurantCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)

class MenuItemCreate(BaseModel):
    restaurant_id: int
    name: str = Field(min_length=2, max_length=120)
    description: str = ""
    price: float = Field(gt=0)
    category: str = Field(min_length=2, max_length=80)
    availability: bool = True

class MenuItemOut(MenuItemCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)

class OrderItemCreate(BaseModel):
    menu_item_id: int
    quantity: int = Field(gt=0)

class OrderCreate(BaseModel):
    restaurant_id: int
    customer_name: str = Field(min_length=2, max_length=120)
    items: List[OrderItemCreate] = Field(min_length=1)

class OrderItemOut(BaseModel):
    id: int
    menu_item_id: int
    quantity: int
    price: float
    model_config = ConfigDict(from_attributes=True)

class OrderOut(BaseModel):
    id: int
    restaurant_id: int
    customer_name: str
    total_amount: float
    status: str
    created_at: datetime
    items: List[OrderItemOut]
    model_config = ConfigDict(from_attributes=True)

class OrderStatusUpdate(BaseModel):
    status: str
