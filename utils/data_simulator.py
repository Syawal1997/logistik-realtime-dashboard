import random
import requests
from datetime import datetime, timedelta
import psycopg2
import streamlit as st

def generate_mock_shipment():
    """Generate mock data shipment untuk simulasi"""
    status_options = ['pending', 'loaded', 'in_transit', 'delivered']
    status = random.choices(status_options, weights=[0.1, 0.2, 0.3, 0.4])[0]
    
    created_at = datetime.now() - timedelta(hours=random.randint(0, 23))
    eta = created_at + timedelta(minutes=random.randint(30, 240))
    
    return {
        'shipment_id': f"SIM-{datetime.now().strftime('%Y%m%d%H%M%S')}-{random.randint(100,999)}",
        'status': status,
        'eta': eta,
        'warehouse_code': random.choice(['WH01', 'WH02', 'WH03']),
        'distance_km': round(random.uniform(5, 100), 2),
        'created_at': created_at,
        'loaded_at': created_at + timedelta(minutes=random.randint(5, 30)) if status in ['loaded', 'in_transit', 'delivered'] else None,
        'arrived_at': created_at + timedelta(minutes=random.randint(30, 180)) if status in ['in_transit', 'delivered'] else None,
        'delivered_at': created_at + timedelta(minutes=random.randint(45, 240)) if status == 'delivered' else None
    }

def run_simulation(interval_seconds=30):
    """Simulasi data masuk setiap 30 detik"""
    conn = psycopg2.connect(st.secrets["database_url"])
    cur = conn.cursor()
    
    for _ in range(10):  # Generate 10 shipments per run
        shipment = generate_mock_shipment()
        
        cur.execute("""
            INSERT INTO shipments 
            (shipment_id, status, eta, warehouse_code, distance_km, 
             created_at, loaded_at, arrived_at, delivered_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (shipment_id) DO NOTHING
        """, (
            shipment['shipment_id'], shipment['status'], shipment['eta'],
            shipment['warehouse_code'], shipment['distance_km'],
            shipment['created_at'], shipment['loaded_at'],
            shipment['arrived_at'], shipment['delivered_at']
        ))
    
    conn.commit()
    cur.close()
    conn.close()
    
    # Update beberapa shipment status
    update_random_statuses()

def update_random_statuses():
    """Update status random shipment untuk simulasi real-time"""
    conn = psycopg2.connect(st.secrets["database_url"])
    cur = conn.cursor()
    
    # Update pending menjadi loaded
    cur.execute("""
        UPDATE shipments 
        SET status = 'loaded', loaded_at = NOW()
        WHERE status = 'pending' 
        AND RANDOM() < 0.3
        LIMIT 5
    """)
    
    # Update loaded menjadi in_transit
    cur.execute("""
        UPDATE shipments 
        SET status = 'in_transit'
        WHERE status = 'loaded' 
        AND RANDOM() < 0.4
        LIMIT 5
    """)
    
    # Update in_transit menjadi delivered
    cur.execute("""
        UPDATE shipments 
        SET status = 'delivered', delivered_at = NOW()
        WHERE status = 'in_transit' 
        AND RANDOM() < 0.5
        LIMIT 5
    """)
    
    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    # Untuk testing simulator
    run_simulation()
