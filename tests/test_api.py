def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_restaurant_menu_and_order_flow(client):
    restaurant = client.post("/api/restaurants", json={
        "name": "Mumbai Spice",
        "address": "Andheri, Mumbai",
        "phone": "9876543210",
        "status": "OPEN",
    })
    assert restaurant.status_code == 201
    restaurant_id = restaurant.json()["id"]

    menu = client.post("/api/menu", json={
        "restaurant_id": restaurant_id,
        "name": "Paneer Tikka",
        "description": "Grilled cottage cheese",
        "price": 220,
        "category": "Starter",
        "availability": True,
    })
    assert menu.status_code == 201
    menu_id = menu.json()["id"]

    order = client.post("/api/orders", json={
        "restaurant_id": restaurant_id,
        "customer_name": "Rahul",
        "items": [{"menu_item_id": menu_id, "quantity": 2}],
    })
    assert order.status_code == 201
    body = order.json()
    assert body["total_amount"] == 440.0
    assert body["status"] == "PLACED"

    status = client.put(f"/api/orders/{body['id']}/status", json={"status": "CONFIRMED"})
    assert status.status_code == 200
    assert status.json()["status"] == "CONFIRMED"

def test_invalid_menu_item_for_order(client):
    restaurant = client.post("/api/restaurants", json={
        "name": "Test Restaurant",
        "address": "Mumbai",
        "phone": "9999999999",
    }).json()

    response = client.post("/api/orders", json={
        "restaurant_id": restaurant["id"],
        "customer_name": "Test",
        "items": [{"menu_item_id": 9999, "quantity": 1}],
    })
    assert response.status_code == 400
