"""
MCP Server for Order Management System.

This MCP server exposes OMS operations as tools that AI assistants can use.
It communicates with the OMS REST API via HTTP.
"""

import httpx
from mcp.server.mcpserver import MCPServer
from pydantic import BaseModel, Field
from typing import Optional

# Configuration
OMS_API_BASE_URL = "http://localhost:8000"

# Create MCP server
mcp = MCPServer("OMS MCP Server")


class OrderItem(BaseModel):
    """An item in an order."""
    product_id: str = Field(description="Unique product identifier")
    product_name: str = Field(description="Name of the product")
    quantity: int = Field(description="Quantity to order", gt=0)
    unit_price: float = Field(description="Price per unit", gt=0)


class ShippingAddress(BaseModel):
    """Shipping address for an order."""
    street: str = Field(description="Street address")
    city: str = Field(description="City")
    state: str = Field(description="State/Province")
    zip_code: str = Field(description="ZIP/Postal code")
    country: str = Field(default="USA", description="Country")


@mcp.tool()
async def place_order(
    customer_id: str,
    items: list[dict],
    shipping_address: dict
) -> dict:
    """
    Place a new order in the Order Management System.
    
    Args:
        customer_id: The unique identifier for the customer placing the order
        items: List of order items, each containing product_id, product_name, quantity, and unit_price
        shipping_address: Shipping address with street, city, state, zip_code, and country
    
    Returns:
        Order confirmation with order details including the generated order_id
    """
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{OMS_API_BASE_URL}/orders",
            json={
                "customer_id": customer_id,
                "items": items,
                "shipping_address": shipping_address
            }
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def get_order_status(order_id: str) -> dict:
    """
    Check the current status of an order.
    
    Args:
        order_id: The unique order identifier (e.g., ORD-001)
    
    Returns:
        Order status information including current status and order_id
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{OMS_API_BASE_URL}/orders/{order_id}/status")
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def get_order_details(order_id: str) -> dict:
    """
    Get full details of an order including items, shipping address, and timestamps.
    
    Args:
        order_id: The unique order identifier (e.g., ORD-001)
    
    Returns:
        Complete order information including items, shipping address, total, and status
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{OMS_API_BASE_URL}/orders/{order_id}")
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def cancel_order(order_id: str) -> dict:
    """
    Cancel an existing order. Only orders with status 'pending' or 'processing' can be cancelled.
    Orders that are already shipped, delivered, or cancelled cannot be cancelled.
    
    Args:
        order_id: The unique order identifier to cancel (e.g., ORD-001)
    
    Returns:
        Cancellation confirmation with updated order details
    """
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{OMS_API_BASE_URL}/orders/{order_id}/cancel")
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def update_order(
    order_id: str,
    items: Optional[list[dict]] = None,
    shipping_address: Optional[dict] = None
) -> dict:
    """
    Update an existing order. Can update items and/or shipping address.
    Only orders with status 'pending' or 'processing' can be updated.
    Orders that are shipped, delivered, or cancelled cannot be updated.
    
    Args:
        order_id: The unique order identifier to update (e.g., ORD-001)
        items: Optional new list of order items to replace existing items
        shipping_address: Optional new shipping address to replace existing address
    
    Returns:
        Updated order details
    """
    update_data = {}
    if items is not None:
        update_data["items"] = items
    if shipping_address is not None:
        update_data["shipping_address"] = shipping_address
    
    async with httpx.AsyncClient() as client:
        response = await client.put(
            f"{OMS_API_BASE_URL}/orders/{order_id}",
            json=update_data
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def list_orders() -> dict:
    """
    List all orders in the system. Useful for getting an overview of existing orders.
    
    Returns:
        List of all orders with their details and total count
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{OMS_API_BASE_URL}/orders")
        response.raise_for_status()
        return response.json()


if __name__ == "__main__":
    # Run with stdio transport (default for MCP)
    mcp.run()
