# Dema

This project is a Dema.ai Backend (data) Hiring Test.

## Setup

1. Clone the repository:

    ```bash
    git clone https://github.com/Jun-Zhang-Data/Dema_Jun_Zhang.git
    cd Dema_Jun_Zhang
    ```

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Create the SQLite database:

    ```bash
    python create_db.py
    ```
4. Run backend:

    ```bash
    python app/backend.py
    ```

## Usage

### List Inventory

Retrieve a paginated list of products in the inventory.

Endpoint: `/list_inventory`

Parameters:
- `limit` (optional): Number of items per page (default: 10)
- `offset` (optional): Page offset (default: 0)
- `category` (optional): Filter by category
- `subcategory` (optional): Filter by subcategory
- `in_stock` (optional): Filter to fetch items in stock (values: `True`, `False`)

Example Q1:
```bash
curl http://localhost:5000/list_inventory
curl http://127.0.0.1:5000/list_inventory?limit=10&offset=0
```

Example Bonus Q1:
```bash
curl http://127.0.0.1:5000/list_inventory?category=Shoes
curl http://127.0.0.1:5000/list_inventory?subcategory=Sneakers
curl http://127.0.0.1:5000/list_inventory?in_stock=True
curl http://127.0.0.1:5000/list_inventory?in_stock=False
```

Example Bonus Q2:
```bash
curl http://127.0.0.1:5000/list_inventory?sort_by=available_quantity
curl http://127.0.0.1:5000/list_inventory?sort_by=total_orders
```

### Update Inventory

The Update Inventory functionality allows you to modify product information in the Inventory.

Endpoint: `/update_product`

### Request Format

Send a PUT request to the endpoint with the following JSON payload:

```json
{
  "products": [
    {
      "productId": "prod1585#prod500001015090",
      "new_name": "Updated Name 1",
      "new_quantity": 555,
	    "new_category": "New category",
	    "new_subCategory": "New subcategory"
    }
  ]
}
```

Example Q2:
```bash
curl -X PUT -H "Content-Type: application/json" -d '{
  "products": [
    {
      "productId": "prod1585#prod500001015090",
      "new_name": "Updated Name 1",
      "new_quantity": 555,
	  "new_category": "New category",
	  "new_subCategory": "New subcategory"
    }
  ]
}' http://localhost:5000/update_product
```

Example Bonus Q3:
```bash
curl -X PUT -H "Content-Type: application/json" -d '{
  "products": [
    {
      "productId": "prod1585#prod500001015090",
      "new_name": "Updated Name 1",
      "new_quantity": 555,
	  "new_category": "New category",
	  "new_subCategory": "New subcategory"
    },
    {
      "productId": "prod1585#prod500001015100",
      "new_name": "Updated Name 2",
      "new_quantity": 300,
	  "new_category": "Second new category",
	  "new_subCategory": "New subcategory2"
    }
  ]
}' http://localhost:5000/update_product
```
## Future work
If given more time some of the following implementations could be done.
1. Additional filtering and sorting capabilities, also more integrations between the orders and the inventory. Now the Orders table is only used to calculate total number of orders. Make sure inventory of product is available when an order is made. 
2. Additional endpoints for updating the Inventory. Currently it is only possible to update the data of an already exisiting product (in the Inventory table). New functionality to add new products or delete existing products should be added. 
