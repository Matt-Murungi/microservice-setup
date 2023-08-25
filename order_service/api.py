import httpx
from typing import List
from fastapi import APIRouter, HTTPException
from .models import (
    OrderCreate,
    Order,
    OrderStatus,
    ProductLocation,
    Product,
)


router = APIRouter()

orders_db = {}
order_id_counter = 1


@router.post("/request/", response_model=Order)
def create_order(order_data: OrderCreate):
    global order_id_counter
    order_id = order_id_counter
    order_id_counter += 1
    if not order_data.products and len(order_data.products) == 0:
        raise HTTPException(status_code=422, detail="Product list cannot be empty")

    assigned_products = []
    for product in order_data.products:
        # Assign location based on customer id
        if order_data.customer_id % 3 == 0:
            product_location = ProductLocation.WAREHOUSE_KISAASI
        elif order_data.customer_id % 3 == 1:
            product_location = ProductLocation.WAREHOUSE_MUKONO
        else:
            product_location = ProductLocation.WAREHOUSE_WAKISO

        assigned_product = Product(
            product_id=product.product_id,
            quantity=product.quantity,
            location=product_location,
        )
        assigned_products.append(assigned_product)

    new_order = Order(
        order_id=order_id,
        customer_id=order_data.customer_id,
        products=assigned_products,
        order_status=OrderStatus.PENDING,
    )
    orders_db[order_id] = new_order
    return new_order


@router.post("/alert-shipping/")
async def alert_shipping(order_data: OrderCreate):
    shipping_alert_data = {
        "order_id": order_data.order_id,
        "customer_id": order_data.customer_id,
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://127.0.0.1:8080/api/shipping/receive", json=shipping_alert_data
            )
            response.raise_for_status()
    except httpx.HTTPError as e:
        raise HTTPException(
            status_code=500, detail=f"Error alerting Shipping Service, {e}"
        )

    return {"message": "Alert sent to Shipping service"}


@router.post("/notify/")
async def notify_notification_service(order_data: OrderCreate):
    notification_data = {
        "order_id": order_data.order_id,
        "status": "pending",
    }
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://127.0.0.1:8081/notifications/send", json=notification_data
            )
            response.raise_for_status()
    except httpx.HTTPError as e:
        raise HTTPException(
            status_code=500, detail=f"Error notifying Notification Service, {e}"
        )

    return {"message": "Notification sent to Notification Service"}


@router.get("/{order_id}", response_model=Order)
def get_order(order_id: int):
    if order_id not in orders_db:
        raise HTTPException(status_code=404, detail="Order not found")
    return orders_db[order_id]


@router.get("/", response_model=List[Order])
def get_all_orders():
    return list(orders_db.values())


def update_order(order_id: int, order_data: Order):
    if order_id not in orders_db:
        raise HTTPException(status_code=404, detail="Order not found")
    orders_db[order_id] = order_data
    return order_data


def delete_order(order_id: int):
    if order_id not in orders_db:
        raise HTTPException(status_code=404, detail="Order not found")
    deleted_order = orders_db.pop(order_id)
    return deleted_order
