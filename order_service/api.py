from fastapi import APIRouter, HTTPException
from .models import OrderCreate, Order, OrderStatus, ProductLocation, Product


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


@router.get("/{order_id}", response_model=Order)
def get_order(order_id: int):
    if order_id not in orders_db:
        raise HTTPException(status_code=404, detail="Order not found")
    return orders_db[order_id]


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
