import sqlite3 as sql

def createDB():
    try:
        conn = sql.connect("products.db")
        conn.commit()
    except sql.Error as e:
        print("Error creating database:", e)
    finally:
        conn.close()

def createTable():
    try:
        conn = sql.connect("products.db")
        cursor = conn.cursor()
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS products (
                name TEXT,
                description TEXT,
                price FLOAT,
                tag TEXT,
                ID TEXT
            )"""
        )
        conn.commit()
    except sql.Error as e:
        print("Error creating table:", e)
    finally:
        conn.close()

def insertRow_product(name, description, price, tag, id):
    try:
        conn = sql.connect("products.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO products (name, description, price, tag, ID) VALUES (?, ?, ?, ?, ?)", (name, description, price, tag, id))
        conn.commit()
    except sql.Error as e:
        print("Error inserting row:", e)
    finally:
        conn.close()

def check_table_structure():
    try:
        conn = sql.connect("products.db")
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(products)")
        columns = cursor.fetchall()
        print(columns)
    except sql.Error as e:
        print("Error checking table structure:", e)
    finally:
        conn.close()

def obtener_productos_existentes():
    try:
        conn = sql.connect("products.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM products")
        productos = cursor.fetchall()
        
        productos_list = []
        for producto in productos:
            producto_dict = {
                "name": producto[0],
                "description": producto[1],
                "price": producto[2],
                "tag": producto[3],
                "ID": producto[4]
            }
            productos_list.append(producto_dict)
        
        return productos_list
    except sql.Error as e:
        print("Error obteniendo productos existentes:", e)
    finally:
        conn.close()


def get_product_by_id(product_id):
    try:
        conn = sql.connect("products.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM products WHERE ID=?", (product_id,))
        product = cursor.fetchone()
        return product
    except sql.Error as e:
        print("Error getting product by ID:", e)
    finally:
        conn.close()

def update_product(product_id, name, description, price, tag):
    try:
        conn = sql.connect("products.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE products SET name=?, description=?, price=?, tag=? WHERE ID=?", (name, description, price, tag, product_id))
        conn.commit()
        return True 
    except sql.Error as e:
        print("Error updating product:", e)
        return False
    finally:
        conn.close()

def delete_product_from_db(product_id):
    try:
        conn = sql.connect("products.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM products WHERE ID=?", (product_id,))
        conn.commit()
    except sql.Error as e:
        print("Error deleting product:", e)
    finally:
        conn.close()
        
if __name__ == "__main__":
    createDB()
    createTable()
    check_table_structure()