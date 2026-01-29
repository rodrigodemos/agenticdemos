import json
import os
from datetime import datetime
from typing import Optional

DATA_FILE_PATH = os.path.join(os.path.dirname(__file__), "data", "orders.json")


def load_orders() -> dict:
    """Load orders from the JSON file."""
    with open(DATA_FILE_PATH, "r") as f:
        return json.load(f)


def save_orders(data: dict) -> None:
    """Save orders to the JSON file."""
    with open(DATA_FILE_PATH, "w") as f:
        json.dump(data, f, indent=2, default=str)


def get_order_by_id(order_id: str) -> Optional[dict]:
    """Get a specific order by ID."""
    data = load_orders()
    for order in data["orders"]:
        if order["order_id"] == order_id:
            return order
    return None


def generate_order_id() -> str:
    """Generate a new unique order ID."""
    data = load_orders()
    if not data["orders"]:
        return "ORD-001"
    
    # Extract numeric parts and find the max
    max_num = 0
    for order in data["orders"]:
        order_num = int(order["order_id"].split("-")[1])
        if order_num > max_num:
            max_num = order_num
    
    return f"ORD-{max_num + 1:03d}"


def create_order(customer_id: str, items: list, shipping_address: dict) -> dict:
    """Create a new order and save it to the file."""
    data = load_orders()
    
    order_id = generate_order_id()
    total_amount = sum(item["quantity"] * item["unit_price"] for item in items)
    now = datetime.utcnow().isoformat() + "Z"
    
    new_order = {
        "order_id": order_id,
        "customer_id": customer_id,
        "status": "pending",
        "items": items,
        "total_amount": round(total_amount, 2),
        "shipping_address": shipping_address,
        "created_at": now,
        "updated_at": now
    }
    
    data["orders"].append(new_order)
    save_orders(data)
    
    return new_order


def update_order(order_id: str, items: Optional[list] = None, shipping_address: Optional[dict] = None) -> Optional[dict]:
    """Update an existing order."""
    data = load_orders()
    
    for i, order in enumerate(data["orders"]):
        if order["order_id"] == order_id:
            # Cannot update cancelled or delivered orders
            if order["status"] in ["cancelled", "delivered"]:
                return None
            
            if items is not None:
                order["items"] = items
                order["total_amount"] = round(
                    sum(item["quantity"] * item["unit_price"] for item in items), 2
                )
            
            if shipping_address is not None:
                order["shipping_address"] = shipping_address
            
            order["updated_at"] = datetime.utcnow().isoformat() + "Z"
            data["orders"][i] = order
            save_orders(data)
            
            return order
    
    return None


def cancel_order(order_id: str) -> Optional[dict]:
    """Cancel an existing order."""
    data = load_orders()
    
    for i, order in enumerate(data["orders"]):
        if order["order_id"] == order_id:
            # Cannot cancel already cancelled, shipped, or delivered orders
            if order["status"] in ["cancelled", "shipped", "delivered"]:
                return None
            
            order["status"] = "cancelled"
            order["updated_at"] = datetime.utcnow().isoformat() + "Z"
            data["orders"][i] = order
            save_orders(data)
            
            return order
    
    return None
