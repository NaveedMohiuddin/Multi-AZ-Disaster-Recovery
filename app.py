from flask import Flask, render_template, request, jsonify
import pymysql
import boto3
import requests
from datetime import datetime

app = Flask(__name__)

# Database configuration
DB_HOST = 'order-system-db.cudaay82ikno.us-east-1.rds.amazonaws.com'
DB_USER = 'admin'
DB_PASSWORD = 'OrderSystem123!'
DB_NAME = 'orderdb'

def get_db_connection():
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        cursorclass=pymysql.cursors.DictCursor
    )

def get_instance_metadata():
    try:
        # Get instance metadata
        response = requests.get('http://169.254.169.254/latest/meta-data/placement/availability-zone', timeout=2)
        az = response.text
        
        response = requests.get('http://169.254.169.254/latest/meta-data/instance-id', timeout=2)
        instance_id = response.text
        
        return {'az': az, 'instance_id': instance_id}
    except:
        return {'az': 'Unknown', 'instance_id': 'Unknown'}

@app.route('/')
def index():
    metadata = get_instance_metadata()
    return render_template('index.html', metadata=metadata)

@app.route('/submit_order', methods=['POST'])
def submit_order():
    try:
        data = request.get_json()
        metadata = get_instance_metadata()
        
        connection = get_db_connection()
        cursor = connection.cursor()
        
        cursor.execute("""
            INSERT INTO orders (customer_name, product_name, quantity, total_price, region, availability_zone)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            data['customer_name'],
            data['product_name'],
            data['quantity'],
            data['total_price'],
            'us-east-1',
            metadata['az']
        ))
        
        connection.commit()
        order_id = cursor.lastrowid
        
        cursor.close()
        connection.close()
        
        return jsonify({
            'success': True,
            'order_id': order_id,
            'message': 'Order submitted successfully!',
            'served_by_az': metadata['az']
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        })

@app.route('/get_orders')
def get_orders():
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        
        cursor.execute("SELECT * FROM orders ORDER BY order_date DESC")
        orders = cursor.fetchall()
        
        cursor.execute("SELECT COUNT(*) as total FROM orders")
        total = cursor.fetchone()['total']
        
        cursor.execute("SELECT SUM(total_price) as revenue FROM orders")
        revenue = cursor.fetchone()['revenue'] or 0
        
        cursor.close()
        connection.close()
        
        return jsonify({
            'success': True,
            'orders': orders,
            'stats': {
                'total_orders': total,
                'total_revenue': float(revenue)
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        })

@app.route('/clear_orders', methods=['POST'])
def clear_orders():
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        
        cursor.execute("DELETE FROM orders")
        connection.commit()
        
        cursor.close()
        connection.close()
        
        return jsonify({
            'success': True,
            'message': 'All orders cleared successfully!'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        })

@app.route('/health')
def health():
    try:
        metadata = get_instance_metadata()
        
        # Test database connection
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        cursor.close()
        connection.close()
        
        return jsonify({
            'status': 'healthy',
            'instance_id': metadata['instance_id'],
            'availability_zone': metadata['az'],
            'database': 'connected',
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)