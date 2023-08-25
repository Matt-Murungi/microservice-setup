from fastapi.testclient import TestClient
from .main import app
from .models import ProductLocation

client = TestClient(app)


def test_create_order():
    customer_id = 123
    products = [
        {
            "product_id": 1,
            "quantity": 2,
        }
    ]
    order_data = {"customer_id": customer_id, "products": products}
    response = client.post("/orders/request/", json=order_data)
    assert response.status_code == 200
    order = response.json()
    assert order["customer_id"] == customer_id
    assert len(order["products"]) == len(products)
    assert order["products"][0]["location"] in [
        ProductLocation.WAREHOUSE_KISAASI,
        ProductLocation.WAREHOUSE_MUKONO,
        ProductLocation.WAREHOUSE_WAKISO,
    ]


def test_empty_products():
    order_data = {"customer_id": 123, "products": []}
    response = client.post("/orders/request/", json=order_data)
    assert response.status_code == 422
