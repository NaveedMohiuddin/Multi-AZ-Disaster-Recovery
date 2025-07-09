import pymysql
#Database Setup Script for Multi-AZ Order System
# Database configuration
DB_HOST = 'YOUR_RDS_ENDPOINT_HERE'  # Replace with your actual RDS endpoint
DB_USER = 'admin'
DB_PASSWORD = 'OrderSystem123!'

try:
    # Connect to MySQL server (without specifying database)
    connection = pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD
    )
    
    cursor = connection.cursor()
    
    # Create database
    cursor.execute("CREATE DATABASE IF NOT EXISTS orderdb")
    cursor.execute("USE orderdb")
    
    # Create table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INT AUTO_INCREMENT PRIMARY KEY,
            customer_name VARCHAR(100) NOT NULL,
            product_name VARCHAR(100) NOT NULL,
            quantity INT NOT NULL,
            total_price DECIMAL(10,2) NOT NULL,
            order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            region VARCHAR(20) NOT NULL
            availability_zone VARCHAR(20)
        )
    """)
    
    connection.commit()
    print("Database and table created successfully!")
    
except Exception as e:
    print(f"Error: {e}")
    
finally:
    if connection:
        connection.close()