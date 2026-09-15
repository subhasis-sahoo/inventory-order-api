def test_create_order(client):
    user_response = client.post(
        "/users/",
        json={
            "name": "Order User",
            "email": "orderuser@example.com"
        }
    )

    user_id = user_response.json()["id"]
    assert user_response.status_code == 201

    product_response = client.post(
        "/products/",
        json={
            "name": "Laptop",
            "description": "Test Laptop",
            "price": 50000,
            "stock": 10
        }
    )

    product_id = product_response.json()["id"]
    assert product_response.status_code == 201

    response = client.post(
        "/orders/",
        json={
            "user_id": user_id,
            "items": [
                {
                    "product_id": product_id,
                    "quantity": 2
                }
            ]
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert "id" in data
    assert data["user_id"] == user_id
    assert data["total_amount"] == 100000
    assert len(data["order_items"]) == 1
    assert data["order_items"][0]["product_id"] == product_id
    assert data["order_items"][0]["quantity"] == 2



def test_create_order_reduces_stock(client):
    user_response = client.post(
        "/users/",
        json={
            "name": "Order User",
            "email": "orderuser@example.com"
        }
    )

    user_id = user_response.json()["id"]

    product_response = client.post(
        "/products/",
        json={
            "name": "Laptop",
            "description": "Test Laptop",
            "price": 52000,
            "stock": 10
        }
    )

    product_id = product_response.json()["id"]

    order_response = client.post(
        "/orders/",
        json={
            "user_id": user_id,
            "items": [
                {
                    "product_id": product_id,
                    "quantity": 4
                }
            ]
        }
    )

    assert order_response.status_code == 201

    product_response = client.get(
        f"/products/{product_id}"
    )

    product_data = product_response.json()

    assert product_data["stock"] == 6



def test_create_order_nonexistent_user(client):
    product_response = client.post(
        "/products/",
        json={
            "name": "Laptop",
            "description": "Test Laptop",
            "price": 50000,
            "stock": 10
        }
    )

    product_id = product_response.json()["id"]

    response = client.post(
        "/orders/",
        json={
            "user_id": 9999,
            "items": [
                {
                    "product_id": product_id,
                    "quantity": 1
                }
            ]
        }
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "User not found"
    }


def test_create_order_nonexistent_product(client):
    user_response = client.post(
        "/users/",
        json={
            "name": "Order User",
            "email": "orderproduct@example.com"
        }
    )

    user_id = user_response.json()["id"]

    response = client.post(
        "/orders/",
        json={
            "user_id": user_id,
            "items": [
                {
                    "product_id": 9999,
                    "quantity": 1
                }
            ]
        }
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Product 9999 not found"
    }


def test_create_order_insufficient_stock(client):
    user_response = client.post(
        "/users/",
        json={
            "name": "Stock User",
            "email": "insufficient@example.com"
        }
    )

    user_id = user_response.json()["id"]

    product_response = client.post(
        "/products/",
        json={
            "name": "Mouse",
            "description": "Test Mouse",
            "price": 500,
            "stock": 2
        }
    )

    product_id = product_response.json()["id"]

    response = client.post(
        "/orders/",
        json={
            "user_id": user_id,
            "items": [
                {
                    "product_id": product_id,
                    "quantity": 5
                }
            ]
        }
    )

    assert response.status_code == 400
    assert response.json() == {
        "detail": f"Insufficient stock for product {product_id}"
    }


def test_get_order(client):
    user_response = client.post(
        "/users/",
        json={
            "name": "Get Order User",
            "email": "getorder@example.com"
        }
    )

    user_id = user_response.json()["id"]

    product_response = client.post(
        "/products/",
        json={
            "name": "Monitor",
            "description": "Test Monitor",
            "price": 20000,
            "stock": 5
        }
    )

    product_id = product_response.json()["id"]

    order_response = client.post(
        "/orders/",
        json={
            "user_id": user_id,
            "items": [
                {
                    "product_id": product_id,
                    "quantity": 1
                }
            ]
        }
    )

    order_id = order_response.json()["id"]

    response = client.get(
        f"/orders/{order_id}"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == order_id
    assert data["user_id"] == user_id
    assert data["total_amount"] == 20000


def test_get_nonexistent_order(client):
    response = client.get("/orders/9999")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Order not found"
    }


def test_get_user_orders(client):
    user_response = client.post(
        "/users/",
        json={
            "name": "Orders User",
            "email": "userorders@example.com"
        }
    )

    user_id = user_response.json()["id"]

    response = client.get(
        f"/users/{user_id}/orders"
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)


# Important business/transaction tests
def test_create_order_multiple_products(client):
    user_response = client.post(
        "/users/",
        json={
            "name": "Order User",
            "email": "userorders@example.com"
        }
    )

    user_id = user_response.json()["id"]

    laptop_response = client.post(
        "/products/",
        json={
            "name": "Laptop",
            "description": "Test Laptop",
            "price": 50000,
            "stock": 10            
        }
    )

    laptop_id = laptop_response.json()["id"]

    monitor_response = client.post(
        "/products/",
        json={
            "name": "Monitor",
            "description": "Test Monitor",
            "price": 20000,
            "stock": 5          
        }
    )

    monitor_id = monitor_response.json()["id"]

    order_response = client.post(
        "/orders/",
        json={
            "user_id": user_id,
            "items": [
                {
                    "product_id": laptop_id,
                    "quantity": 2
                },
                {
                    "product_id": monitor_id,
                    "quantity": 3
                }
            ]
        }
    )

    assert order_response.status_code == 201

    order_data = order_response.json()

    assert order_data["user_id"] == user_id
    assert order_data["total_amount"] == 160000
    assert len(order_data["order_items"]) == 2
    assert order_data["order_items"][0]["product_id"] == laptop_id
    assert order_data["order_items"][0]["quantity"] == 2
    assert order_data["order_items"][1]["product_id"] == monitor_id
    assert order_data["order_items"][1]["quantity"] == 3
    


def test_order_reduces_stock_for_multiple_products(client):
    user_response = client.post(
        "/users/",
        json={
            "name": "Stock User",
            "email": "multistock@example.com"
        }
    )
    user_id = user_response.json()["id"]

    laptop_response = client.post(
        "/products/",
        json={
            "name": "Laptop",
            "description": "Test Laptop",
            "price": 50000,
            "stock": 10
        }
    )
    laptop_id = laptop_response.json()["id"]

    mouse_response = client.post(
        "/products/",
        json={
            "name": "Mouse",
            "description": "Test Mouse",
            "price": 500,
            "stock": 20
        }
    )
    mouse_id = mouse_response.json()["id"]

    response = client.post(
        "/orders/",
        json={
            "user_id": user_id,
            "items": [
                {
                    "product_id": laptop_id,
                    "quantity": 2
                },
                {
                    "product_id": mouse_id,
                    "quantity": 3
                }
            ]
        }
    )

    assert response.status_code == 201

    laptop = client.get(f"/products/{laptop_id}").json()
    mouse = client.get(f"/products/{mouse_id}").json()

    assert laptop["stock"] == 8
    assert mouse["stock"] == 17


def test_create_order_invalid_quantity(client):
    user_response = client.post(
        "/users/",
        json={
            "name": "Invalid Quantity",
            "email": "invalidquantity@example.com"
        }
    )
    user_id = user_response.json()["id"]

    product_response = client.post(
        "/products/",
        json={
            "name": "Keyboard",
            "description": "Test Keyboard",
            "price": 2000,
            "stock": 10
        }
    )
    product_id = product_response.json()["id"]

    response = client.post(
        "/orders/",
        json={
            "user_id": user_id,
            "items": [
                {
                    "product_id": product_id,
                    "quantity": 0
                }
            ]
        }
    )

    assert response.status_code == 422


def test_create_order_negative_quantity(client):
    user_response = client.post(
        "/users/",
        json={
            "name": "Negative Quantity",
            "email": "negativequantity@example.com"
        }
    )
    user_id = user_response.json()["id"]

    product_response = client.post(
        "/products/",
        json={
            "name": "Keyboard",
            "description": "Test Keyboard",
            "price": 2000,
            "stock": 10
        }
    )
    product_id = product_response.json()["id"]

    response = client.post(
        "/orders/",
        json={
            "user_id": user_id,
            "items": [
                {
                    "product_id": product_id,
                    "quantity": -2
                }
            ]
        }
    )

    assert response.status_code == 422


def test_stock_unchanged_when_order_fails(client):
    user_response = client.post(
        "/users/",
        json={
            "name": "Failed Order User",
            "email": "failedorder@example.com"
        }
    )
    user_id = user_response.json()["id"]

    product_response = client.post(
        "/products/",
        json={
            "name": "Mouse",
            "description": "Test Mouse",
            "price": 500,
            "stock": 2
        }
    )
    product_id = product_response.json()["id"]

    response = client.post(
        "/orders/",
        json={
            "user_id": user_id,
            "items": [
                {
                    "product_id": product_id,
                    "quantity": 5
                }
            ]
        }
    )

    assert response.status_code == 400

    product = client.get(f"/products/{product_id}").json()

    assert product["stock"] == 2



def test_failed_order_does_not_partially_reduce_stock(client):
    user_response = client.post(
        "/users/",
        json={
            "name": "Transaction User",
            "email": "transaction@example.com"
        }
    )
    user_id = user_response.json()["id"]

    laptop_response = client.post(
        "/products/",
        json={
            "name": "Laptop",
            "description": "Test Laptop",
            "price": 50000,
            "stock": 10
        }
    )
    laptop_id = laptop_response.json()["id"]

    mouse_response = client.post(
        "/products/",
        json={
            "name": "Mouse",
            "description": "Test Mouse",
            "price": 500,
            "stock": 1
        }
    )
    mouse_id = mouse_response.json()["id"]

    assert mouse_response.json()["stock"] == 1

    response = client.post(
        "/orders/",
        json={
            "user_id": user_id,
            "items": [
                {
                    "product_id": laptop_id,
                    "quantity": 2
                },
                {
                    "product_id": mouse_id,
                    "quantity": 5
                }
            ]
        }
    )

    assert response.status_code == 400

    laptop = client.get(f"/products/{laptop_id}").json()
    mouse = client.get(f"/products/{mouse_id}").json()

    assert laptop["stock"] == 10
    assert mouse["stock"] == 1






