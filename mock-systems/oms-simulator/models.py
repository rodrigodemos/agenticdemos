from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum
from datetime import datetime


class OrderStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


class ShippingAddress(BaseModel):
    street: str
    city: str
    state: str
    zip_code: str
    country: str = "USA"


class OrderItem(BaseModel):
    product_id: str
    product_name: str
    quantity: int = Field(gt=0)
    unit_price: float = Field(gt=0)


class Order(BaseModel):
    order_id: str
    customer_id: str
    status: OrderStatus
    items: List[OrderItem]
    total_amount: float
    shipping_address: ShippingAddress
    created_at: datetime
    updated_at: datetime


class CreateOrderRequest(BaseModel):
    customer_id: str
    items: List[OrderItem]
    shipping_address: ShippingAddress


class UpdateOrderRequest(BaseModel):
    items: Optional[List[OrderItem]] = None
    shipping_address: Optional[ShippingAddress] = None


class OrderResponse(BaseModel):
    success: bool
    message: str
    order: Optional[Order] = None


class OrderStatusResponse(BaseModel):
    success: bool
    order_id: str
    status: Optional[OrderStatus] = None
    message: str
