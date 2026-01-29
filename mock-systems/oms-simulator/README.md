# OMS Simulator

A mock Order Management System API for testing integrations.

## Setup

1. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

2. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Server

```bash
python main.py
```

Or using uvicorn directly:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## API Endpoints

### Health Check
- `GET /` - Returns service health status

### Orders
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/orders` | List all orders |
| POST | `/orders` | Place a new order |
| GET | `/orders/{order_id}` | Get order details |
| GET | `/orders/{order_id}/status` | Check order status |
| PUT | `/orders/{order_id}` | Update an order |
| POST | `/orders/{order_id}/cancel` | Cancel an order |

## Example Requests

### Place a New Order
```bash
curl -X POST http://localhost:8000/orders \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": "CUST-200",
    "items": [
      {
        "product_id": "PROD-010",
        "product_name": "Gaming Mouse",
        "quantity": 1,
        "unit_price": 59.99
      }
    ],
    "shipping_address": {
      "street": "100 Test Ave",
      "city": "Denver",
      "state": "CO",
      "zip_code": "80202",
      "country": "USA"
    }
  }'
```

### Check Order Status
```bash
curl http://localhost:8000/orders/ORD-001/status
```

### Update an Order
```bash
curl -X PUT http://localhost:8000/orders/ORD-001 \
  -H "Content-Type: application/json" \
  -d '{
    "items": [
      {
        "product_id": "PROD-001",
        "product_name": "Wireless Mouse",
        "quantity": 3,
        "unit_price": 29.99
      }
    ]
  }'
```

### Cancel an Order
```bash
curl -X POST http://localhost:8000/orders/ORD-001/cancel
```

## Order Statuses

- `pending` - Order has been placed
- `processing` - Order is being processed
- `shipped` - Order has been shipped
- `delivered` - Order has been delivered
- `cancelled` - Order has been cancelled

## Sample Data

The sample orders are stored in `data/orders.json`. The file is automatically updated when orders are created, updated, or cancelled.

---

## MCP Server

The MCP (Model Context Protocol) server allows AI assistants to interact with the OMS APIs.

### Running the MCP Server

**Important:** The FastAPI server must be running first since the MCP server calls it via HTTP.

1. Start the FastAPI server in one terminal:
   ```bash
   python main.py
   ```

2. The MCP server can be used with AI assistants that support MCP. For stdio transport:
   ```bash
   python mcp_server.py
   ```

### MCP Tools Available

| Tool | Description |
|------|-------------|
| `place_order` | Place a new order with customer ID, items, and shipping address |
| `get_order_status` | Check the current status of an order |
| `get_order_details` | Get full details of an order |
| `cancel_order` | Cancel a pending or processing order |
| `update_order` | Update items or shipping address of an order |
| `list_orders` | List all orders in the system |

### VS Code / GitHub Copilot Configuration

Add this to your MCP settings (e.g., `.vscode/mcp.json`):

```json
{
  "servers": {
    "oms": {
      "command": "python",
      "args": ["path/to/oms-simulator/mcp_server.py"]
    }
  }
}
```

### Example Tool Usage

Once connected, an AI assistant can use commands like:
- "Place an order for customer CUST-200 with 2 wireless keyboards"
- "What's the status of order ORD-001?"
- "Cancel order ORD-002"
- "Update order ORD-001 to ship to a new address"

