import psycopg2
import os
import random
from datetime import datetime, timedelta

# Ambil dari environment variable (untuk GitHub Actions)
DB_URL = os.getenv("DATABASE_URL")

def generate_shipment():
    statuses = ['pending', 'loaded', 'in_transit', 'delivered']
    status = random.choice(statuses)
    
    return (
        f"SIM-{datetime.now().strftime('%H%M%S')}-{random.randint(100,999)}",
        status,
        datetime.now(),
        datetime.now() + timedelta(hours=random.randint(1, 4)),
        random.choice(['WH01', 'WH02', 'WH03']),
        round(random.uniform(5, 100), 2)
    )

def insert_shipment():
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    
    shipment = generate_shipment()
    cur.execute("""
        INSERT INTO shipments (shipment_id, status, created_at, eta, warehouse_code, distance_km)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, shipment)
    
    conn.commit()
    cur.close()
    conn.close()
    print(f"Inserted: {shipment[0]}")

if __name__ == "__main__":
    insert_shipment()
