import requests


BASE_URL = "http://localhost:8080"


def test_login_success():
    response = requests.post(
        f"{BASE_URL}/api/login",
        json={
            "phone": "01012345678",
            "password": "test1234"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["resultType"] == "SUCCESS"
    assert data["success"]["accessToken"] == "mock-access-token"
    assert data["success"]["userId"] == "1001"


def test_login_both_missing():
    response = requests.post(
        f"{BASE_URL}/api/login",
        json={}
    )

    assert response.status_code == 400

    data = response.json()

    assert data["resultType"] == "FAIL"
    assert data["error"]["errorCode"] == "INVALID_REQUEST"


def test_login_phone_missing():
    response = requests.post(
        f"{BASE_URL}/api/login",
        json={
            "phone": "",
            "password": "test1234"
        }
    )

    assert response.status_code == 400

    data = response.json()

    assert data["resultType"] == "FAIL"
    assert data["error"]["errorCode"] == "INVALID_REQUEST"


def test_login_password_missing():
    response = requests.post(
        f"{BASE_URL}/api/login",
        json={
            "phone": "01012345678",
            "password": ""
        }
    )

    assert response.status_code == 400

    data = response.json()

    assert data["resultType"] == "FAIL"
    assert data["error"]["errorCode"] == "INVALID_REQUEST"


def test_login_invalid_credential():
    response = requests.post(
        f"{BASE_URL}/api/login",
        json={
            "phone": "01012345678",
            "password": "wrong1234"
        }
    )

    assert response.status_code == 401

    data = response.json()

    assert data["resultType"] == "FAIL"
    assert data["error"]["errorCode"] == "INVALID_CREDENTIALS"


def test_login_server_error():
    response = requests.post(
        f"{BASE_URL}/api/login",
        headers={
            "X-Mock-Scenario": "server-error"
        },
        json={
            "phone": "01012345678",
            "password": "test1234"
        }
    )

    assert response.status_code == 500

    data = response.json()

    assert data["resultType"] == "FAIL"
    assert data["error"]["errorCode"] == "INTERNAL_SERVER_ERROR"