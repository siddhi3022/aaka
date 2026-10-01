import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from app.database import get_db
from app.models import MenuItem, Order, OrderItem, Restaurant
from app.schemas import OrderCreate, OrderOut, OrderStatusUpdate

logger = logging.getLogger("food-ordering")

ALLOWED_STATUSES = {"PLACED", "CONFIRMED", "PREPARING", "READY", "DELIVERED", "CANCELLED"}

router = APIRouter(prefix="/api/orders", tags=["Orders"])

@router.post("", response_model=OrderOut, status_code=201)
def create_order(data: OrderCreate, db: Session = Depends(get_db)):
    if not db.get(Restaurant, data.restaurant_id):
        raise HTTPException(status_code=404, detail="Restaurant not found")

    order = Order(
        restaurant_id=data.restaurant_id,
        customer_name=data.customer_name,
        total_amount=0,
        status="PLACED",
    )
    db.add(order)
    db.flush()

    total = 0.0
    for requested in data.items:
        item = db.get(MenuItem, requested.menu_item_id)
        if not item or item.restaurant_id != data.restaurant_id:
            raise HTTPException(status_code=400, detail=f"Invalid menu item: {requested.menu_item_id}")
        if not item.availability:
            raise HTTPException(status_code=400, detail=f"Menu item unavailable: {item.name}")

        line_total = item.price * requested.quantity
        total += line_total
        db.add(OrderItem(
            order_id=order.id,
            menu_item_id=item.id,
            quantity=requested.quantity,
            price=item.price,
        ))

    order.total_amount = round(total, 2)
    db.commit()
    db.refresh(order)
    logger.info("Order created: id=%s total=%.2f", order.id, order.total_amount)

    return db.query(Order).options(joinedload(Order.items)).filter(Order.id == order.id).first()

@router.get("", response_model=list[OrderOut])
def list_orders(db: Session = Depends(get_db)):
    return db.query(Order).options(joinedload(Order.items)).order_by(Order.id.desc()).all()

@router.get("/{order_id}", response_model=OrderOut)
def get_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).options(joinedload(Order.items)).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router.put("/{order_id}/status", response_model=OrderOut)
def update_order_status(order_id: int, data: OrderStatusUpdate, db: Session = Depends(get_db)):
    if data.status not in ALLOWED_STATUSES:
        raise HTTPException(status_code=400, detail="Invalid order status")
    order = db.get(Order, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    order.status = data.status
    db.commit()
    db.refresh(order)
    logger.info("Order status changed: id=%s status=%s", order.id, order.status)
    return db.query(Order).options(joinedload(Order.items)).filter(Order.id == order.id).first()
