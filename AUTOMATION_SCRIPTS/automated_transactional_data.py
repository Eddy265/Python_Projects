import random
import psycopg2
from datetime import date, timedelta

# PostgreSQL database connection parameters
db_params = {
    "host": "your_postgres_host",
    "database": "your_database_name",
    "user": "your_username",
    "password": "your_password",
}

# Number of random records to insert
num_records = 1000

def generate_random_date(start_date, end_date):
    time_delta = end_date - start_date
    random_days = random.randint(0, time_delta.days)
    return start_date + timedelta(days=random_days)

def generate_random_data():
    customer_ids = list(range(1, 1001))
    order_statuses = ["pending", "processing", "shipped", "delivered"]

    for _ in range(num_records):
        order_id = random.randint(100000, 999999)
        customer_id = random.choice(customer_ids)
        order_dow = random.randint(0, 6)
        order_hour_of_day = random.randint(0, 23)
        days_since_prior_order = random.randint(1, 30)
        product_id = random.randint(1000, 9999)
        quantity = random.randint(1, 10)
        order_date = generate_random_date(date(2023, 1, 1), date(2023, 7, 31))
        order_status = random.choice(order_statuses)

        yield (order_id, customer_id, order_dow, order_hour_of_day, days_since_prior_order,
               product_id, quantity, order_date, order_status)

def insert_data():
    try:
        conn = psycopg2.connect(**db_params)
        cur = conn.cursor()

        insert_query = """
            INSERT INTO public.orders (
                order_id, customer_id, order_dow, order_hour_of_day,
                days_since_prior_order, product_id, quantity, order_date, order_status
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        for data in generate_random_data():
            cur.execute(insert_query, data)

        conn.commit()
        print(f"{num_records} random records inserted into the 'orders' table successfully.")

    except (Exception, psycopg2.DatabaseError) as error:
        print("Error:", error)
    finally:
        if conn is not None:
            conn.close()

if __name__ == "__main__":
    insert_data()
