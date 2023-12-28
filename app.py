from flask import Flask, render_template
from flask import request
import sqlite3

app = Flask(__name__)

DATABASE = "Trendyol.db"
def create_database():
    # Connect to SQLite database (creates a new database file if it doesn't exist)
    conn = sqlite3.connect(DATABASE )
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_no INTEGER NOT NULL,
            description TEXT NOT NULL,
            price REAL NOT NULL,
            image_url TEXT NOT NULL,
            category TEXT NOT NULL
        )
    """
    )
    conn.commit()
    conn.close()
    
def insert_sample_data():
    # Connect to SQLite database
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Check if sample data already exists
    cursor.execute("SELECT COUNT(*) FROM products")
    count = cursor.fetchone()[0]

    if count == 0:
        # Insert sample data for at least 10 products
        products = [
            (1, 'çizgili triko kazak', 88.99, "images/product1.webp", 'Kazak'),
            (2, 'Palazzo pantolon', 249.99, "images/product2.webp", 'Pantolon'),
            (3, 'Unisex yılbaşı çorap', 65.35, "images/product3.webp", 'Çorap'),
            (4, 'Pamuklu Pijama Takım', 185.91, "images/product4.webp", 'Pijama'),
            (5, 'Siyah Kadın Bot', 300, "images/product5.webp", 'Bot'),
            (6, 'Yüksek bel tayt', 153.99, "images/product6.webp", 'Tayt'),
            (7, ' El Ele Tutuşan çorap', 64.99, "images/product7.webp", 'Çorap'),
            (8, 'Pijama takım', 181.99, "images/product8.webp", 'Pijama'),
            (9, 'Renkli  Mandal toka 5', 36.49, "images/product9.webp", 'Toka'),
            (10, 'Jogger  eşofman', 180.99, "images/product10.webp", 'Eşofman'),
        ]

        # Insert the sample data
        cursor.executemany(
            """
            INSERT INTO products (product_no, description, price, image_url, category)
            VALUES (?, ?, ?, ?, ?)
            """,
            products
        )

        # Commit the changes
        conn.commit()

    # Close the connection
    conn.close()


    

@app.route('/')
def index():
    create_database()
    insert_sample_data()

    

    # Connect to SQLite database
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Fetch products for the current page
    cursor.execute('SELECT * FROM products')
    products = cursor.fetchall()

    # Close the connection
    conn.close()

    # Render the template with the list of products and page information
    return render_template('index.html', products=products)
    # Add a new route for advantageous products


@app.route('/product/<int:product_no>')
def product_detail(product_no):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Fetch the specific product based on product_no
    cursor.execute('SELECT * FROM products WHERE product_no = ?', (product_no,))
    product = cursor.fetchone()

    # Close the connection
    conn.close()

    # Render the template with product details
    return render_template('product_detail.html', product=product)


@app.route('/search')
def search():
    # Get the search query from the URL parameters
    query = request.args.get('query', '')

    # Connect to SQLite database
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Search for products that match the query in any attribute (case-insensitive)
    cursor.execute("SELECT DISTINCT * FROM products WHERE "
               "product_no LIKE ? OR "
               "description LIKE ? OR "
               "price LIKE ? OR "
               "category LIKE ? COLLATE NOCASE",
               ('%' + query + '%', '%' + query + '%', '%' + query + '%', '%' + query + '%'))

    search_results = cursor.fetchall()

    # Close the connection
    conn.close()

    # Render the template with the search results
    return render_template('search.html', query=query, search_results=search_results)

    # Close the connection
    conn.close()

    # Render the template with the search results
    return render_template('search.html', query=query, search_results=search_results)


if __name__ == '__main__':
     
     app.run(debug=True)