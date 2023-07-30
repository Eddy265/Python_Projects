import random
import psycopg2
from datetime import date, timedelta
import schedule
import time

# PostgreSQL database connection parameters
db_params = {
    "host": "localhost",
    "database": "Instacart",
    "user": "postgres",
    "password": "database password",
}

# Number of records to insert in each iteration
num_records = 5

def generate_random_date(start_date, end_date):
    time_delta = end_date - start_date
    random_days = random.randint(0, time_delta.days)
    return start_date + timedelta(days=random_days)

def get_max_order_id():
    conn = psycopg2.connect(**db_params)
    cur = conn.cursor()
    cur.execute("SELECT MAX(order_id) FROM public.orders")
    max_order_id = cur.fetchone()[0]
    conn.close()
    return max_order_id or 3422084  # Return 3422084 if no records exist

def generate_sequential_data(start_order_id):
    customer_ids = list(range(1, 1001))
    order_statuses = ["Processing", "Shipped", "Delivered"]

    for i in range(num_records):
        order_id = start_order_id + i
        customer_id = random.choice(customer_ids)
        order_dow = random.randint(0, 6)
        order_hour_of_day = random.randint(0, 23)
        days_since_prior_order = random.randint(1, 30)
        product_id = random.randint(1, 49688)
        quantity = random.randint(1, 10)
        order_date = generate_random_date(date(2023, 1, 1), date(2023, 7, 31))
        order_status = random.choice(order_statuses)

        yield (order_id, customer_id, order_dow, order_hour_of_day, days_since_prior_order,
               product_id, quantity, order_date, order_status)

def insert_data():
    try:
        # Get the current maximum order_id from the table
        start_order_id = get_max_order_id()

        conn = psycopg2.connect(**db_params)
        cur = conn.cursor()

        insert_query = """
            INSERT INTO public.orders (
                order_id, customer_id, order_dow, order_hour_of_day,
                days_since_prior_order, product_id, quantity, order_date, order_status
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        for data in generate_sequential_data(start_order_id + 1):
            cur.execute(insert_query, data)

        conn.commit()
        print(f"{num_records} Transactions successful.")

    except (Exception, psycopg2.DatabaseError) as error:
        print("Error:", error)
    finally:
        if conn is not None:
            conn.close()

def run_job():
    # Insert data into the 'orders' table every 1 minute
    insert_data()

if __name__ == "__main__":
    # Schedule the job to run every 1 minute
    schedule.every(1).minutes.do(run_job)

    while True:
        schedule.run_pending()
        time.sleep(1)
