import pandas as pd
import sqlite3
from pathlib import Path

def create_database():
    # Path to the database file
    db_path = 'db/inventory.db'

    # Check if the database file exists
    db_file = Path(db_path)
    if db_file.exists():
        # If the file exists, delete it
        db_file.unlink()

    # Create a new SQLite database
    db_file.touch()

def read_csv_to_dataframe(file_path):
    # Reads a CSV file and returns a DataFrame
    return pd.read_csv(file_path, nrows=1)

def infer_table_schema(df, table_name):
    # Infers the schema of a table from a DataFrame
    return f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join([f'{col} {df[col].dtype}' for col in df.columns])})"

def create_table(cursor, create_table_sql):
    # Creates a table in the database
    cursor.execute(create_table_sql)

def insert_data_into_table(df, table_name, conn):
    # Inserts data from a DataFrame into a table in the database
    df.to_sql(table_name, conn, if_exists='replace', index=False)

def print_table_rows(cursor, table_name):
    # Prints the rows of a table in the database
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()

    for row in rows:
        print(row)

def main():
    create_database()

    # Connect to SQLite database (creates it if not exists)
    conn = sqlite3.connect('db/inventory.db')
    cursor = conn.cursor()

    # Read the CSV files
    df_order = read_csv_to_dataframe('data/orders.csv')
    df_inventory = read_csv_to_dataframe('data/inventory.csv')

    # Generate and execute CREATE TABLE statements
    create_order_table_sql = infer_table_schema(df_order, 'Orders')
    create_inventory_table_sql = infer_table_schema(df_inventory, 'Inventory')

    create_table(cursor, create_order_table_sql)
    create_table(cursor, create_inventory_table_sql)

    # Insert data into tables
    insert_data_into_table(pd.read_csv("data/orders.csv"), 'Orders', conn)
    insert_data_into_table(pd.read_csv("data/inventory.csv"), 'Inventory', conn)

    # Print the rows of the tables
    print_table_rows(cursor, 'Orders')
    print_table_rows(cursor, 'Inventory')

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

if __name__ == '__main__':
    main()
