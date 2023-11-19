from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

DATABASE = '../db/inventory.db'

def row_to_dict(row):
    return dict(zip(row.keys(), row))

def get_db():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db


@app.route('/list_inventory')
def list_inventory():
    # Extracting pagination parameters from the request
    limit = request.args.get('limit', default=10, type=int)
    offset = request.args.get('offset', default=0, type=int)

    # Extracting filter parameters from the request
    category_filter = request.args.get('category')
    subcategory_filter = request.args.get('subcategory')
    in_stock_filter = request.args.get('in_stock')

    # Extracting sorting parameter from the request
    sort_by = request.args.get('sort_by', default='available_quantity')

    with get_db() as db:
        cursor = db.cursor()

        # Build the query based on filters
        query = '''
            SELECT 
                Inventory.productId AS productId,
                Inventory.name AS name,
                Inventory.quantity AS available_quantity,
                Inventory.category AS category,
                Inventory.subCategory AS subCategory,
                SUM(Orders.quantity) AS total_orders
            FROM Inventory
            INNER JOIN Orders ON Inventory.productId = Orders.productId
        '''

        # Apply filters
        filters = []
        if category_filter:
            filters.append("Inventory.category = '{}'".format(category_filter))
        if subcategory_filter:
            filters.append("Inventory.subCategory = '{}'".format(subcategory_filter))
        if in_stock_filter:
            if in_stock_filter == 'True':
                filters.append("Inventory.quantity > 0")
            else:
                filters.append("Inventory.quantity == 0")

        if filters:
            query += ' WHERE ' + ' AND '.join(filters)

        # Apply sorting with aliasing
        if sort_by in ['available_quantity', 'total_orders']:
            query += ' GROUP BY Inventory.productId ORDER BY {} DESC LIMIT ? OFFSET ?;'.format(sort_by)
        else:
            query += ' GROUP BY Inventory.productId ORDER BY Inventory.productId LIMIT ? OFFSET ?;'

        cursor.execute(query, (limit, offset))
        data = cursor.fetchall()

    # Convert the sqlite3.Row objects to dictionaries
    data_dicts = [row_to_dict(row) for row in data]

    return jsonify(data_dicts)


# Update_product function that can handle bulk updates
def update_product(product_id, new_name, new_quantity, new_category, new_subCategory):
    with get_db() as db:
        cursor = db.cursor()
        # Update the product information
        cursor.execute('''
            UPDATE Inventory
            SET name = ?,
                quantity = ?,
                category = ?,
                subCategory = ?
            WHERE productId = ?;
        ''', (new_name, new_quantity, new_category, new_subCategory, product_id))

        # Get the updated product and its order data
        cursor.execute('''
            SELECT 
                Inventory.productId AS productId,
                Inventory.name AS name,
                Inventory.quantity AS available_quantity,
                Inventory.category AS category,
                Inventory.subCategory AS subCategory,
                SUM(Orders.quantity) AS total_orders
            FROM Inventory
            LEFT JOIN Orders ON Inventory.productId = Orders.productId
            WHERE Inventory.productId = ?
            GROUP BY Inventory.productId;
        ''', (product_id,))

        updated_data = cursor.fetchone()

    if updated_data:
        return row_to_dict(updated_data)
    else:
        return {'error': 'Product not found'}, 404

# Modify update_product_endpoint to handle bulk updates
@app.route('/update_product', methods=['PUT'])
def update_product_endpoint():
    try:
        products_to_update = request.json['products']
    except KeyError:
        return jsonify({'error': 'Invalid input'}), 400

    updated_products = []
    for product in products_to_update:
        product_id = product['productId']
        new_name = product.get('new_name')
        new_quantity = product.get('new_quantity')
        new_category = product.get('new_category')
        new_subCategory = product.get('new_subCategory')

        updated_product = update_product(product_id, new_name, new_quantity, new_category, new_subCategory)
        updated_products.append(updated_product)

    return jsonify(updated_products)


if __name__ == '__main__':
    app.run(debug=True)