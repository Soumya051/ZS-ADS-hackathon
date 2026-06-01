
import sqlite3
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

DB_FOLDER = os.environ['DB_FOLDER']
DB_NAME = os.environ['DB_NAME']
DB_PATH = Path(DB_FOLDER) / DB_NAME


def setup_database():

    Path(DB_FOLDER).mkdir(exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Orders Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        order_id TEXT PRIMARY KEY,
        customer_id TEXT NOT NULL,
        status TEXT NOT NULL,
        created_at TEXT,
        estimated_delivery TEXT,
        tracking_number TEXT,
        shipping_address_id TEXT NOT NULL,
        total_amount REAL NOT NULL,
        payment_method TEXT NOT NULL
    )
    """)

    # Items Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS items (
        item_id TEXT PRIMARY KEY,
        order_id TEXT NOT NULL,
        product_id TEXT NOT NULL,
        product_name TEXT NOT NULL,
        quantity INTEGER NOT NULL,
        unit_price REAL NOT NULL,
        status TEXT NOT NULL,

        FOREIGN KEY(order_id)
        REFERENCES orders(order_id)
    )
    """)

    # Customers Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS customers (
        customer_id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        phone TEXT NOT NULL,
        tier TEXT,
        preferred_refund_method TEXT
    )
    """)

    # Address Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS addresses (
        address_id TEXT PRIMARY KEY,
        customer_id TEXT NOT NULL,
        label TEXT,
        line1 TEXT NOT NULL,
        line2 TEXT,
        city TEXT NOT NULL,
        state TEXT NOT NULL,
        pincode TEXT NOT NULL,

        FOREIGN KEY(customer_id)
        REFERENCES customers(customer_id)
    )
    """)

    # Cases Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cases (
        case_id TEXT PRIMARY KEY,
        customer_id TEXT NOT NULL,
        order_id TEXT NOT NULL,
        status TEXT NOT NULL,
        priority TEXT NOT NULL,
        description TEXT,
        amount_inr REAL,
        trace_id TEXT,
        created_at TEXT,

        FOREIGN KEY(customer_id)
        REFERENCES customers(customer_id),

        FOREIGN KEY(order_id)
        REFERENCES orders(order_id)
    )
    """)

    #Kb_articles Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS kb_articles (
        article_id TEXT PRIMARY KEY,
        title TEXT NON NULL,
        tags TEXT NON NULL,
        content TEXT NON NULL,
        last_updated TEXT NON NULL,
        applies_to TEXT NON NULL
    )
    """)

    #Payment_config Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS queries (
        query_id TEXT PRIMARY KEY,
        customer_id TEXT NON NULL,
        order_id TEXT NON NULL,
        status TEXT NON NULL,
        user_query TEXT NON NULL,
        intent TEXT NON NULL,
        intent_details TEXT
    )
    """)

    #Payment_config Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS payment_config (
        auto_refund_limit_inr INTEGER NOT NULL,
        supported_method TEXT NON NULL,
        refund_sla_days INTEGER NON NULL,
        behaviour TEXT NON NULL
    )
    """)

    conn.commit()
    conn.close()

    print("Database setup complete.")
