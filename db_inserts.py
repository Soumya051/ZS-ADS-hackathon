
import sqlite3
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

DB_FOLDER = os.environ['DB_FOLDER']
DB_NAME = os.environ['DB_NAME']
DB_PATH = Path(DB_FOLDER) / DB_NAME

def get_connection():
    return sqlite3.connect(DB_PATH)

def validate_shapes(*args):

    # Check if arguments are lists
    are_lists = [isinstance(arg, list) for arg in args]

    # Ensure all are same type (all lists or all single values)
    if len(set(are_lists)) != 1:
        raise ValueError(
            "All inputs must either be single values "
            "or lists of equal length."
        )

    # If lists, ensure equal lengths
    if are_lists[0]:

        lengths = [len(arg) for arg in args]

        if len(set(lengths)) != 1:
            raise ValueError(
                "All input lists must have the same length."
            )

    return


def execute_insert(conn, query, rows):

    cursor = conn.cursor()

    if isinstance(rows[0], tuple):
        cursor.executemany(query, rows)
    else:
        cursor.execute(query, rows)

    conn.commit()


def insert_orders(
    connection,
    order_id,
    customer_id,
    status,
    created_at,
    estimated_delivery,
    tracking_number,
    shipping_address_id,
    total_amount,
    payment_method
):

    validate_shapes(
        order_id,
        customer_id,
        status,
        created_at,
        estimated_delivery,
        tracking_number,
        shipping_address_id,
        total_amount,
        payment_method
    )

    query = """
    INSERT INTO orders VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """

    if isinstance(order_id, list):

        rows = list(zip(
            order_id,
            customer_id,
            status,
            created_at,
            estimated_delivery,
            tracking_number,
            shipping_address_id,
            total_amount,
            payment_method
        ))

    else:

        rows = (
            order_id,
            customer_id,
            status,
            created_at,
            estimated_delivery,
            tracking_number,
            shipping_address_id,
            total_amount,
            payment_method
        )

    execute_insert(connection, query, rows)


def insert_items(
    connection,
    item_id,
    order_id,
    product_id,
    product_name,
    quantity,
    unit_price,
    status
):

    validate_shapes(
        item_id,
        order_id,
        product_id,
        product_name,
        quantity,
        unit_price,
        status
    )

    query = """
    INSERT INTO items VALUES (?, ?, ?, ?, ?, ?, ?)
    """

    if isinstance(item_id, list):

        rows = list(zip(
            item_id,
            order_id,
            product_id,
            product_name,
            quantity,
            unit_price,
            status
        ))

    else:

        rows = (
            item_id,
            order_id,
            product_id,
            product_name,
            quantity,
            unit_price,
            status
        )

    execute_insert(connection, query, rows)


def insert_customers(
    connection,
    customer_id,
    name,
    email,
    phone,
    tier,
    preferred_refund_method
):

    validate_shapes(
        customer_id,
        name,
        email,
        phone,
        tier,
        preferred_refund_method
    )

    query = """
    INSERT INTO customers VALUES (?, ?, ?, ?, ?, ?)
    """

    if isinstance(customer_id, list):

        rows = list(zip(
            customer_id,
            name,
            email,
            phone,
            tier,
            preferred_refund_method
        ))

    else:

        rows = (
            customer_id,
            name,
            email,
            phone,
            tier,
            preferred_refund_method
        )

    execute_insert(connection, query, rows)


def insert_addresses(
    connection,
    address_id,
    customer_id,
    label,
    line1,
    line2,
    city,
    state,
    pincode
):

    validate_shapes(
        address_id,
        customer_id,
        label,
        line1,
        line2,
        city,
        state,
        pincode
    )

    query = """
    INSERT INTO addresses VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """

    if isinstance(address_id, list):

        rows = list(zip(
            address_id,
            customer_id,
            label,
            line1,
            line2,
            city,
            state,
            pincode
        ))

    else:

        rows = (
            address_id,
            customer_id,
            label,
            line1,
            line2,
            city,
            state,
            pincode
        )

    execute_insert(connection, query, rows)


def insert_cases(
    connection,
    case_id,
    customer_id,
    order_id,
    status,
    priority,
    description,
    amount_inr,
    trace_id,
    created_at
):

    validate_shapes(
        case_id,
        customer_id,
        order_id,
        status,
        priority,
        description,
        amount_inr,
        trace_id,
        created_at
    )

    query = """
    INSERT INTO cases VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """

    if isinstance(case_id, list):

        rows = list(zip(
            case_id,
            customer_id,
            order_id,
            status,
            priority,
            description,
            amount_inr,
            trace_id,
            created_at
        ))

    else:

        rows = (
            case_id,
            customer_id,
            order_id,
            status,
            priority,
            description,
            amount_inr,
            trace_id,
            created_at
        )

    execute_insert(connection, query, rows)


def insert_kb_articles(
    connection,
    article_id,
    title,
    tags,
    content,
    last_updated,
    applies_to
):

    query = """
    INSERT INTO kb_articles VALUES (?, ?, ?, ?, ?, ?)
    """

    validate_shapes(
        article_id,
        title,
        tags,
        content,
        last_updated,
        applies_to
    )

    if isinstance(article_id, list):

        rows = list(zip(
            article_id,
            title,
            tags,
            content,
            last_updated,
            applies_to
        ))

    else:

        rows = (
            article_id,
            title,
            tags,
            content,
            last_updated,
            applies_to
        )

    execute_insert(connection, query, rows)

def insert_queries(
    connection,
    query_id,
    customer_id,
    order_id,
    status,
    user_query
):

    query = """
    INSERT INTO queries VALUES (?, ?, ?, ?, ?)
    """

    validate_shapes(
        query_id,
        customer_id,
        order_id,
        status,
        user_query
    )

    if isinstance(query_id, list):

        rows = list(zip(
            query_id,
            customer_id,
            order_id,
            status,
            user_query
            ))


    else:

        rows = (
            query_id,
            customer_id,
            order_id,
            status,
            user_query
        )

    execute_insert(connection, query, rows)

def insert_payment_config(
    connection,
    auto_refund_limit_inr,
    supported_method,
    refund_sla_days,
    behaviour
):

    query = """
    INSERT INTO payment_config VALUES (?, ?, ?, ?)
    """

    validate_shapes(
        auto_refund_limit_inr,
        supported_method,
        refund_sla_days,
        behaviour
    )

    if isinstance(auto_refund_limit_inr, list):

        rows = list(zip(
            auto_refund_limit_inr,
            supported_method,
            refund_sla_days,
            behaviour
        ))


    else:

        rows = (
            auto_refund_limit_inr,
            supported_method,
            refund_sla_days,
            behaviour
        )

    execute_insert(connection, query, rows)
