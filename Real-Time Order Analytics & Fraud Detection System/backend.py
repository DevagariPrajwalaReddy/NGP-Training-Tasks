import psycopg2
from psycopg2.extras import execute_batch
from fastapi import FastAPI, Request
from pydantic import BaseModel
import pandas as pd

# DB config
DB_CONFIG = {
    'host': 'localhost',
    'database': 'ecommerce',
    'user': 'postgres',
    'password': 'root'
}

app = FastAPI() # FastAPI application instance

class Order(BaseModel):
    order_id: str
    user_id: str
    product_id: str
    quantity: int
    price: float
    payment_mode: str
    order_ts: str
    delivery_city: str

def insert_orders_into_db(orders):
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    
    insert_query = """
    INSERT INTO orders (order_id, user_id, product_id, quantity, price, payment_mode, order_ts, delivery_city)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (order_id) DO NOTHING;
    """
    # - ON CONFLICT (order_id): This specifies that if there's a conflict (i.e., a duplicate value) in the order_id column
    # - DO NOTHING: ...then do nothing. Don't insert the row, and don't throw an error.
    
    order_values = [
        (
            o.order_id, o.user_id, o.product_id, o.quantity, o.price,
            o.payment_mode, o.order_ts, o.delivery_city
        )
        for o in orders
    ]
    
    try:

        """ execute_batch: This is a function from psycopg2.extras that executes a single query 
        with multiple sets of parameters (i.e., batch execution).
        - cur: The cursor object.
        - insert_query: The SQL query to execute (with placeholders %s).
        - order_values: A list of tuples """

        """  
            Instead of using execute_batch we can also opt for:
                for values in order_values:
                    cur.execute(insert_query, values)
        """
        execute_batch(cur, insert_query, order_values)
        conn.commit()
        print(f"Inserted {len(order_values)} orders")

    except Exception as e:
        print(f"DB error: {e}")
        conn.rollback()
        
    finally:
        cur.close()
        conn.close()

def get_daily_revenue():
    conn = psycopg2.connect(**DB_CONFIG)
    query = """
    SELECT DATE(order_ts), SUM(price * quantity) 
    FROM orders 
    GROUP BY 1;
    """
    # GROUP BY 1 means "group by the first column in the SELECT clause", which is DATE(order_ts)
    df = pd.read_sql(query, conn)
    return df.to_dict(orient='records')

    """ The orient parameter determines the output format. Some common options:

    - orient='dict': Returns a dictionary with column names as keys and dictionaries as values.
    - orient='list': Returns a dictionary with column names as keys and lists as values.
    - orient='records': Returns a list of dictionaries, as shown above.
    - orient='index': Returns a dictionary with index values as keys and dictionaries as values. 
    
    """
def get_top_users():
    conn = psycopg2.connect(**DB_CONFIG)
    query = """
    SELECT user_id, SUM(price * quantity) 
    FROM orders 
    WHERE order_ts > NOW() - INTERVAL '7 days'
    GROUP BY 1 
    ORDER BY 2 DESC 
    LIMIT 10;
    """
    df = pd.read_sql(query, conn)
    return df.to_dict(orient='records')

def detect_fraud():
    conn = psycopg2.connect(**DB_CONFIG)
    query = """
    SELECT user_id, COUNT(*) 
    FROM orders 
    WHERE order_ts > NOW() - INTERVAL '10 minutes'
    GROUP BY 1 
    HAVING COUNT(*) > 5;
    """
    df = pd.read_sql(query, conn)
    suspicious_users = df['user_id'].tolist()
    return suspicious_users

# API endpoints
@app.post("/orders/")
async def create_order(order: Order):
    insert_orders_into_db([order])
    return {"message": "Order created"}

@app.post("/orders/batch/")
async def create_orders(request: Request):
    data = await request.json()
    orders = [Order(**o) for o in data]
    insert_orders_into_db(orders)
    return {"message": f"{len(orders)} orders created"}

@app.get("/metrics/daily-revenue")
def daily_revenue():
    data = get_daily_revenue()
    return data

@app.get("/metrics/top-users")
def top_users():
    data = get_top_users()
    return data

@app.get("/fraud/alerts")
def fraud_alerts():
    data = detect_fraud()
    return data
