def test_create_product(client):
    response = client.post(
        "/products/",
        json={
            "name": "Laptop",
            "description": "Test Laptop",
            "price": 50000,
            "stock": 10
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert data["name"] == "Laptop"
    assert data["description"] == "Test Laptop"
    assert data["price"] == 50000
    assert data["stock"] == 10
    assert "id" in data


def test_create_product_invalid_price(client):
    response = client.post(
        "/products/",
        json={
            "name": "Laptop",
            "description": "Test Laptop",
            "price": -50000,
            "stock": 10            
        }
    )

    assert response.status_code == 422


def test_create_product_invalid_stock(client):
    response = client.post(
        "/products/",
        json={
            "name": "Laptop",
            "description": "Test Laptop",
            "price": 50000,
            "stock": -10            
        }
    )

    assert response.status_code == 422


def test_get_products(client):
    response = client.get("/products/")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)


def test_get_product(client):
    response = client.post(
        "/products/",
        json={
            "name": "Laptop",
            "description": "Test Laptop",
            "price": 50000,
            "stock": 10
        }
    )

    data = response.json()

    product_id = data["id"]


    response2 = client.get(f"/products/{product_id}")

    assert response2.status_code == 200

    data2 = response2.json()

    assert data2["id"] == product_id
    assert data2["name"] == "Laptop"
    assert data2["description"] == "Test Laptop"
    assert data2["price"] == 50000
    assert data2["stock"] == 10



def test_get_nonexistent_product(client):
    response = client.get("/products/200")

    assert response.status_code == 404

    assert response.json() == {
        "detail": "Product not found"
    }



def test_filter_products_by_name(client):
    client.post(
        "/products/",
        json={
            "name": "Laptop",
            "description": "Test Laptop",
            "price": 50000,
            "stock": 10
        }
    )

    client.post(
        "/products/",
        json={
            "name": "Mouse",
            "description": "Test Mouse",
            "price": 500,
            "stock": 6
        }
    )

    response = client.get("/products/?name=Laptop")

    assert response.status_code == 200

    data = response.json()

    assert data[0]["name"] == "Laptop"
    assert data[0]["description"] == "Test Laptop"
    assert data[0]["price"] == 50000
    assert data[0]["stock"] == 10
    assert "id" in data[0]



def test_filter_products_by_min_price(client):
    client.post(
        "/products/",
        json={
            "name": "Laptop",
            "description": "Test Laptop",
            "price": 50000,
            "stock": 10
        }
    )

    client.post(
        "/products/",
        json={
            "name": "Mouse",
            "description": "Test Mouse",
            "price": 500,
            "stock": 6
        }
    )


    response = client.get("/products/?min_price=10000")
    
    assert response.status_code == 200

    data = response.json()

    assert data[0]["name"] == "Laptop"
    assert data[0]["description"] == "Test Laptop"
    assert data[0]["price"] == 50000
    assert data[0]["stock"] == 10
    assert "id" in data[0]



def test_update_product(client):
    create_response = client.post(
        "/products/",
        json={
            "name": "Laptop",
            "description": "Old Laptop",
            "price": 50000,
            "stock": 10
        }
    )

    product_id = create_response.json()["id"]

    response = client.put(
        f"/products/{product_id}",
        json={
            "name": "Gaming Laptop",
            "description": "Updated Laptop",
            "price": 75000,
            "stock": 15
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == product_id
    assert data["name"] == "Gaming Laptop"
    assert data["description"] == "Updated Laptop"
    assert data["price"] == 75000
    assert data["stock"] == 15


def test_update_nonexistent_product(client):
    response = client.put(
        "/products/9999",
        json={
            "name": "Laptop",
            "description": "Test Laptop",
            "price": 50000,
            "stock": 10
        }
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Product not found"
    }



def test_patch_product(client):
    create_response = client.post(
        "/products/",
        json={
            "name": "Laptop",
            "description": "Test Laptop",
            "price": 50000,
            "stock": 10
        }
    )

    product_id = create_response.json()["id"]

    response = client.patch(
        f"/products/{product_id}",
        json={
            "price": 60000
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == product_id
    assert data["price"] == 60000
    assert data["name"] == "Laptop"
    assert data["stock"] == 10



def test_delete_product(client):
    create_response = client.post(
        "/products/",
        json={
            "name": "Laptop",
            "description": "Test Laptop",
            "price": 50000,
            "stock": 10
        }
    )

    product_id = create_response.json()["id"]

    response = client.delete(
        f"/products/{product_id}"
    )

    assert response.status_code == 200

    assert response.json() == {
        "message": "Product Deleted From The List"
    }


def test_delete_nonexistent_product(client):
    response = client.delete("/products/9999")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Product not found"
    }