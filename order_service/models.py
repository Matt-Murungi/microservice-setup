from pydantic import BaseModel
from typing import List
from enum import Enum


class ProductLocation(str, Enum):
    WAREHOUSE_KISAASI = "WAREHOUSE_KISAASI"
    WAREHOUSE_MUKONO = "WAREHOUSE_MUKONO"
    WAREHOUSE_WAKISO = "WAREHOUSE_WAKISO"


class OrderStatus(str, Enum):
    PENDING = "PENDING"
    CANCELLED = "CANCELLED"
    COMPLETE = "COMPLETE"


class Product(BaseModel):
    product_id: int
    quantity: int
    location: ProductLocation = None


class OrderCreate(BaseModel):
    customer_id: int
    products: List[Product]


class Order(BaseModel):
    order_id: int
    customer_id: int
    products: List[Product]
    order_status: OrderStatus = None


