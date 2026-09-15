def test_create_user(client):
    response = client.post(
        "/users/",
        json={
            "name": "Test User",
            "email": "testuser@example.com"
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert data["name"] == "Test User"
    assert data["email"] == "testuser@example.com"
    assert "id" in data


def test_create_user_invalid_email(client):
    response = client.post(
        "/users/",
        json={
            "name": "Test User2",
            "email": "testuser2example.com"
        }
    )

    assert response.status_code == 422

    data = response.json()

    assert data["detail"][0]["loc"] == ["body", "email"]



def test_create_user_duplicate_email(client):
    client.post(
        "/users/",
        json={
            "name": "Test User3",
            "email": "testuser@example.com"
        }
    )

    response = client.post(
            "/users/",
            json={
                "name": "Test User3",
                "email": "testuser@example.com"
            }
        )

    assert response.status_code == 409

    assert response.json() == {
        "detail": "Email already registered"
    }




def test_get_users(client):
    response = client.get("/users/")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)


def test_get_nonexistent_user(client):
    response = client.get("/users/400")

    assert response.status_code == 404

    assert response.json() == {
        "detail": "User not found"
    }

