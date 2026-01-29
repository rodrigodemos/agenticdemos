from fastapi import FastAPI, HTTPException
from models import (
    CreateOrderRequest,
    UpdateOrderRequest,
    OrderResponse,
    OrderStatusResponse,
    Order,
    OrderStatus
)
from data_service import (
    get_order_by_id,
    create_order,
    update_order,
    cancel_order,
    load_orders
)

app = FastAPI(
    title="Order Management System Simulator",
    description="A mock OMS API for testing integrations",
    version="1.0.0"
)


@app.get("/")
def root():
    """Health check endpoint."""
    return {"status": "healthy", "service": "OMS Simulator"}


@app.get("/orders", response_model=dict)
def list_orders():
    """List all orders (for debugging/testing purposes)."""
    data = load_orders()
    return {"orders": data["orders"], "count": len(data["orders"])}


@app.post("/orders", response_model=OrderResponse)
def place_order(request: CreateOrderRequest):
    """
    Place a new order.
    
    Creates a new order with the provided customer, items, and shipping details.
    The order will be created with 'pending' status.
    """
    items_dict = [item.model_dump() for item in request.items]
    shipping_dict = request.shipping_address.model_dump()
    
    new_order = create_order(
        customer_id=request.customer_id,
        items=items_dict,
        shipping_address=shipping_dict
    )
    
    return OrderResponse(
        success=True,
        message=f"Order {new_order['order_id']} created successfully",
        order=Order(**new_order)
    )


@app.get("/orders/{order_id}/status", response_model=OrderStatusResponse)
def check_order_status(order_id: str):
    """
    Check the status of an order.
    
    Returns the current status of the specified order.
    """
    order = get_order_by_id(order_id)
    
    if not order:
        raise HTTPException(status_code=404, detail=f"Order {order_id} not found")
    
    return OrderStatusResponse(
        success=True,
        order_id=order_id,
        status=OrderStatus(order["status"]),
        message=f"Order status: {order['status']}"
    )


@app.get("/orders/{order_id}", response_model=OrderResponse)
def get_order(order_id: str):
    """
    Get full order details.
    
    Returns complete information about the specified order.
    """
    order = get_order_by_id(order_id)
    
    if not order:
        raise HTTPException(status_code=404, detail=f"Order {order_id} not found")
    
    return OrderResponse(
        success=True,
        message="Order retrieved successfully",
        order=Order(**order)
    )


@app.put("/orders/{order_id}", response_model=OrderResponse)
def update_order_endpoint(order_id: str, request: UpdateOrderRequest):
    """
    Update an existing order.
    
    Allows updating items and/or shipping address.
    Cannot update cancelled or delivered orders.
    """
    order = get_order_by_id(order_id)
    
    if not order:
        raise HTTPException(status_code=404, detail=f"Order {order_id} not found")
    
    if order["status"] in ["cancelled", "delivered"]:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot update order with status '{order['status']}'"
        )
    
    items_dict = [item.model_dump() for item in request.items] if request.items else None
    shipping_dict = request.shipping_address.model_dump() if request.shipping_address else None
    
    updated_order = update_order(
        order_id=order_id,
        items=items_dict,
        shipping_address=shipping_dict
    )
    
    if not updated_order:
        raise HTTPException(status_code=400, detail="Failed to update order")
    
    return OrderResponse(
        success=True,
        message=f"Order {order_id} updated successfully",
        order=Order(**updated_order)
    )


@app.post("/orders/{order_id}/cancel", response_model=OrderResponse)
def cancel_order_endpoint(order_id: str):
    """
    Cancel an existing order.
    
    Changes the order status to 'cancelled'.
    Cannot cancel orders that are already cancelled, shipped, or delivered.
    """
    order = get_order_by_id(order_id)
    
    if not order:
        raise HTTPException(status_code=404, detail=f"Order {order_id} not found")
    
    if order["status"] in ["cancelled", "shipped", "delivered"]:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot cancel order with status '{order['status']}'"
        )
    
    cancelled_order = cancel_order(order_id)
    
    if not cancelled_order:
        raise HTTPException(status_code=400, detail="Failed to cancel order")
    
    return OrderResponse(
        success=True,
        message=f"Order {order_id} has been cancelled",
        order=Order(**cancelled_order)
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
