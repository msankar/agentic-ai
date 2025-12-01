import pandas as pd
import numpy as np
import os
import time
import dotenv
import ast
from sqlalchemy.sql import text
from datetime import datetime, timedelta
from typing import Dict, List, Union
from sqlalchemy import create_engine, Engine
import logging
import json

# Create an SQLite database
db_engine = create_engine("sqlite:///munder_difflin.db")

# List containing the different kinds of papers 
paper_supplies = [
    # Paper Types (priced per sheet unless specified)
    {"item_name": "A4 paper",                         "category": "paper",        "unit_price": 0.05},
    {"item_name": "Letter-sized paper",              "category": "paper",        "unit_price": 0.06},
    {"item_name": "Cardstock",                        "category": "paper",        "unit_price": 0.15},
    {"item_name": "Colored paper",                    "category": "paper",        "unit_price": 0.10},
    {"item_name": "Glossy paper",                     "category": "paper",        "unit_price": 0.20},
    {"item_name": "Matte paper",                      "category": "paper",        "unit_price": 0.18},
    {"item_name": "Recycled paper",                   "category": "paper",        "unit_price": 0.08},
    {"item_name": "Eco-friendly paper",               "category": "paper",        "unit_price": 0.12},
    {"item_name": "Poster paper",                     "category": "paper",        "unit_price": 0.25},
    {"item_name": "Banner paper",                     "category": "paper",        "unit_price": 0.30},
    {"item_name": "Kraft paper",                      "category": "paper",        "unit_price": 0.10},
    {"item_name": "Construction paper",               "category": "paper",        "unit_price": 0.07},
    {"item_name": "Wrapping paper",                   "category": "paper",        "unit_price": 0.15},
    {"item_name": "Glitter paper",                    "category": "paper",        "unit_price": 0.22},
    {"item_name": "Decorative paper",                 "category": "paper",        "unit_price": 0.18},
    {"item_name": "Letterhead paper",                 "category": "paper",        "unit_price": 0.12},
    {"item_name": "Legal-size paper",                 "category": "paper",        "unit_price": 0.08},
    {"item_name": "Crepe paper",                      "category": "paper",        "unit_price": 0.05},
    {"item_name": "Photo paper",                      "category": "paper",        "unit_price": 0.25},
    {"item_name": "Uncoated paper",                   "category": "paper",        "unit_price": 0.06},
    {"item_name": "Butcher paper",                    "category": "paper",        "unit_price": 0.10},
    {"item_name": "Heavyweight paper",                "category": "paper",        "unit_price": 0.20},
    {"item_name": "Standard copy paper",              "category": "paper",        "unit_price": 0.04},
    {"item_name": "Bright-colored paper",             "category": "paper",        "unit_price": 0.12},
    {"item_name": "Patterned paper",                  "category": "paper",        "unit_price": 0.15},

    # Product Types (priced per unit)
    {"item_name": "Paper plates",                     "category": "product",      "unit_price": 0.10},  # per plate
    {"item_name": "Paper cups",                       "category": "product",      "unit_price": 0.08},  # per cup
    {"item_name": "Paper napkins",                    "category": "product",      "unit_price": 0.02},  # per napkin
    {"item_name": "Disposable cups",                  "category": "product",      "unit_price": 0.10},  # per cup
    {"item_name": "Table covers",                     "category": "product",      "unit_price": 1.50},  # per cover
    {"item_name": "Envelopes",                        "category": "product",      "unit_price": 0.05},  # per envelope
    {"item_name": "Sticky notes",                     "category": "product",      "unit_price": 0.03},  # per sheet
    {"item_name": "Notepads",                         "category": "product",      "unit_price": 2.00},  # per pad
    {"item_name": "Invitation cards",                 "category": "product",      "unit_price": 0.50},  # per card
    {"item_name": "Flyers",                           "category": "product",      "unit_price": 0.15},  # per flyer
    {"item_name": "Party streamers",                  "category": "product",      "unit_price": 0.05},  # per roll
    {"item_name": "Decorative adhesive tape (washi tape)", "category": "product", "unit_price": 0.20},  # per roll
    {"item_name": "Paper party bags",                 "category": "product",      "unit_price": 0.25},  # per bag
    {"item_name": "Name tags with lanyards",          "category": "product",      "unit_price": 0.75},  # per tag
    {"item_name": "Presentation folders",             "category": "product",      "unit_price": 0.50},  # per folder

    # Large-format items (priced per unit)
    {"item_name": "Large poster paper (24x36 inches)", "category": "large_format", "unit_price": 1.00},
    {"item_name": "Rolls of banner paper (36-inch width)", "category": "large_format", "unit_price": 2.50},

    # Specialty papers
    {"item_name": "100 lb cover stock",               "category": "specialty",    "unit_price": 0.50},
    {"item_name": "80 lb text paper",                 "category": "specialty",    "unit_price": 0.40},
    {"item_name": "250 gsm cardstock",                "category": "specialty",    "unit_price": 0.30},
    {"item_name": "220 gsm poster paper",             "category": "specialty",    "unit_price": 0.35},
]

# Given below are some utility functions you can use to implement your multi-agent system

def generate_sample_inventory(paper_supplies: list, coverage: float = 0.4, seed: int = 137) -> pd.DataFrame:
    """
    Generate inventory for exactly a specified percentage of items from the full paper supply list.

    This function randomly selects exactly `coverage` × N items from the `paper_supplies` list,
    and assigns each selected item:
    - a random stock quantity between 200 and 800,
    - a minimum stock level between 50 and 150.

    The random seed ensures reproducibility of selection and stock levels.

    Args:
        paper_supplies (list): A list of dictionaries, each representing a paper item with
                               keys 'item_name', 'category', and 'unit_price'.
        coverage (float, optional): Fraction of items to include in the inventory (default is 0.4, or 40%).
        seed (int, optional): Random seed for reproducibility (default is 137).

    Returns:
        pd.DataFrame: A DataFrame with the selected items and assigned inventory values, including:
                      - item_name
                      - category
                      - unit_price
                      - current_stock
                      - min_stock_level
    """
    # Ensure reproducible random output
    np.random.seed(seed)

    # Calculate number of items to include based on coverage
    num_items = int(len(paper_supplies) * coverage)

    # Randomly select item indices without replacement
    selected_indices = np.random.choice(
        range(len(paper_supplies)),
        size=num_items,
        replace=False
    )

    # Extract selected items from paper_supplies list
    selected_items = [paper_supplies[i] for i in selected_indices]

    # Construct inventory records
    inventory = []
    for item in selected_items:
        inventory.append({
            "item_name": item["item_name"],
            "category": item["category"],
            "unit_price": item["unit_price"],
            "current_stock": np.random.randint(200, 800),  # Realistic stock range
            "min_stock_level": np.random.randint(50, 150)  # Reasonable threshold for reordering
        })

    # Return inventory as a pandas DataFrame
    return pd.DataFrame(inventory)

def init_database(db_engine: Engine, seed: int = 137) -> Engine:    
    """
    Set up the Munder Difflin database with all required tables and initial records.

    This function performs the following tasks:
    - Creates the 'transactions' table for logging stock orders and sales
    - Loads customer inquiries from 'quote_requests.csv' into a 'quote_requests' table
    - Loads previous quotes from 'quotes.csv' into a 'quotes' table, extracting useful metadata
    - Generates a random subset of paper inventory using `generate_sample_inventory`
    - Inserts initial financial records including available cash and starting stock levels

    Args:
        db_engine (Engine): A SQLAlchemy engine connected to the SQLite database.
        seed (int, optional): A random seed used to control reproducibility of inventory stock levels.
                              Default is 137.

    Returns:
        Engine: The same SQLAlchemy engine, after initializing all necessary tables and records.

    Raises:
        Exception: If an error occurs during setup, the exception is printed and raised.
    """
    try:
        # ----------------------------
        # 1. Create an empty 'transactions' table schema
        # ----------------------------
        transactions_schema = pd.DataFrame({
            "id": [],
            "item_name": [],
            "transaction_type": [],  # 'stock_orders' or 'sales'
            "units": [],             # Quantity involved
            "price": [],             # Total price for the transaction
            "transaction_date": [],  # ISO-formatted date
        })
        transactions_schema.to_sql("transactions", db_engine, if_exists="replace", index=False)

        # Set a consistent starting date
        initial_date = datetime(2025, 1, 1).isoformat()

        # ----------------------------
        # 2. Load and initialize 'quote_requests' table
        # ----------------------------
        quote_requests_df = pd.read_csv("data/quote_requests.csv")
        quote_requests_df["id"] = range(1, len(quote_requests_df) + 1)
        quote_requests_df.to_sql("quote_requests", db_engine, if_exists="replace", index=False)

        # ----------------------------
        # 3. Load and transform 'quotes' table
        # ----------------------------
        quotes_df = pd.read_csv("data/quotes.csv")
        quotes_df["request_id"] = range(1, len(quotes_df) + 1)
        quotes_df["order_date"] = initial_date

        # Unpack metadata fields (job_type, order_size, event_type) if present
        if "request_metadata" in quotes_df.columns:
            quotes_df["request_metadata"] = quotes_df["request_metadata"].apply(
                lambda x: ast.literal_eval(x) if isinstance(x, str) else x
            )
            quotes_df["job_type"] = quotes_df["request_metadata"].apply(lambda x: x.get("job_type", ""))
            quotes_df["order_size"] = quotes_df["request_metadata"].apply(lambda x: x.get("order_size", ""))
            quotes_df["event_type"] = quotes_df["request_metadata"].apply(lambda x: x.get("event_type", ""))

        # Retain only relevant columns
        quotes_df = quotes_df[[
            "request_id",
            "total_amount",
            "quote_explanation",
            "order_date",
            "job_type",
            "order_size",
            "event_type"
        ]]
        quotes_df.to_sql("quotes", db_engine, if_exists="replace", index=False)

        # ----------------------------
        # 4. Generate inventory and seed stock
        # ----------------------------
        inventory_df = generate_sample_inventory(paper_supplies, seed=seed)

        # Seed initial transactions
        initial_transactions = []

        # Add a starting cash balance via a dummy sales transaction
        initial_transactions.append({
            "item_name": None,
            "transaction_type": "sales",
            "units": None,
            "price": 50000.0,
            "transaction_date": initial_date,
        })

        # Add one stock order transaction per inventory item
        for _, item in inventory_df.iterrows():
            initial_transactions.append({
                "item_name": item["item_name"],
                "transaction_type": "stock_orders",
                "units": item["current_stock"],
                "price": item["current_stock"] * item["unit_price"],
                "transaction_date": initial_date,
            })

        # Commit transactions to database
        pd.DataFrame(initial_transactions).to_sql("transactions", db_engine, if_exists="append", index=False)

        # Save the inventory reference table
        inventory_df.to_sql("inventory", db_engine, if_exists="replace", index=False)

        return db_engine

    except Exception as e:
        print(f"Error initializing database: {e}")
        raise

def create_transaction(
    item_name: str,
    transaction_type: str,
    quantity: int,
    price: float,
    date: Union[str, datetime],
) -> int:
    """
    This function records a transaction of type 'stock_orders' or 'sales' with a specified
    item name, quantity, total price, and transaction date into the 'transactions' table of the database.

    Args:
        item_name (str): The name of the item involved in the transaction.
        transaction_type (str): Either 'stock_orders' or 'sales'.
        quantity (int): Number of units involved in the transaction.
        price (float): Total price of the transaction.
        date (str or datetime): Date of the transaction in ISO 8601 format.

    Returns:
        int: The ID of the newly inserted transaction.

    Raises:
        ValueError: If `transaction_type` is not 'stock_orders' or 'sales'.
        Exception: For other database or execution errors.
    """
    try:
        # Convert datetime to ISO string if necessary
        date_str = date.isoformat() if isinstance(date, datetime) else date

        # Validate transaction type
        if transaction_type not in {"stock_orders", "sales"}:
            raise ValueError("Transaction type must be 'stock_orders' or 'sales'")

        # Prepare transaction record as a single-row DataFrame
        transaction = pd.DataFrame([{
            "item_name": item_name,
            "transaction_type": transaction_type,
            "units": quantity,
            "price": price,
            "transaction_date": date_str,
        }])

        # Insert the record into the database
        transaction.to_sql("transactions", db_engine, if_exists="append", index=False)

        # Fetch and return the ID of the inserted row
        result = pd.read_sql("SELECT last_insert_rowid() as id", db_engine)
        return int(result.iloc[0]["id"])

    except Exception as e:
        print(f"Error creating transaction: {e}")
        raise

def get_all_inventory(as_of_date: str) -> Dict[str, int]:
    """
    Retrieve a snapshot of available inventory as of a specific date.

    This function calculates the net quantity of each item by summing 
    all stock orders and subtracting all sales up to and including the given date.

    Only items with positive stock are included in the result.

    Args:
        as_of_date (str): ISO-formatted date string (YYYY-MM-DD) representing the inventory cutoff.

    Returns:
        Dict[str, int]: A dictionary mapping item names to their current stock levels.
    """
    # SQL query to compute stock levels per item as of the given date
    query = """
        SELECT
            item_name,
            SUM(CASE
                WHEN transaction_type = 'stock_orders' THEN units
                WHEN transaction_type = 'sales' THEN -units
                ELSE 0
            END) as stock
        FROM transactions
        WHERE item_name IS NOT NULL
        AND transaction_date <= :as_of_date
        GROUP BY item_name
        HAVING stock > 0
    """

    # Execute the query with the date parameter
    result = pd.read_sql(query, db_engine, params={"as_of_date": as_of_date})

    # Convert the result into a dictionary {item_name: stock}
    return dict(zip(result["item_name"], result["stock"]))

def get_stock_level(item_name: str, as_of_date: Union[str, datetime]) -> pd.DataFrame:
    """
    Retrieve the stock level of a specific item as of a given date.

    This function calculates the net stock by summing all 'stock_orders' and 
    subtracting all 'sales' transactions for the specified item up to the given date.

    Args:
        item_name (str): The name of the item to look up.
        as_of_date (str or datetime): The cutoff date (inclusive) for calculating stock.

    Returns:
        pd.DataFrame: A single-row DataFrame with columns 'item_name' and 'current_stock'.
    """
    # Convert date to ISO string format if it's a datetime object
    if isinstance(as_of_date, datetime):
        as_of_date = as_of_date.isoformat()

    # SQL query to compute net stock level for the item
    stock_query = """
        SELECT
            item_name,
            COALESCE(SUM(CASE
                WHEN transaction_type = 'stock_orders' THEN units
                WHEN transaction_type = 'sales' THEN -units
                ELSE 0
            END), 0) AS current_stock
        FROM transactions
        WHERE item_name = :item_name
        AND transaction_date <= :as_of_date
    """

    # Execute query and return result as a DataFrame
    return pd.read_sql(
        stock_query,
        db_engine,
        params={"item_name": item_name, "as_of_date": as_of_date},
    )

def get_supplier_delivery_date(input_date_str: str, quantity: int) -> str:
    """
    Estimate the supplier delivery date based on the requested order quantity and a starting date.

    Delivery lead time increases with order size:
        - ≤10 units: same day
        - 11–100 units: 1 day
        - 101–1000 units: 4 days
        - >1000 units: 7 days

    Args:
        input_date_str (str): The starting date in ISO format (YYYY-MM-DD).
        quantity (int): The number of units in the order.

    Returns:
        str: Estimated delivery date in ISO format (YYYY-MM-DD).
    """
    # Debug log (comment out in production if needed)
    print(f"FUNC (get_supplier_delivery_date): Calculating for qty {quantity} from date string '{input_date_str}'")

    # Attempt to parse the input date
    try:
        input_date_dt = datetime.fromisoformat(input_date_str.split("T")[0])
    except (ValueError, TypeError):
        # Fallback to current date on format error
        print(f"WARN (get_supplier_delivery_date): Invalid date format '{input_date_str}', using today as base.")
        input_date_dt = datetime.now()

    # Determine delivery delay based on quantity
    if quantity <= 10:
        days = 0
    elif quantity <= 100:
        days = 1
    elif quantity <= 1000:
        days = 4
    else:
        days = 7

    # Add delivery days to the starting date
    delivery_date_dt = input_date_dt + timedelta(days=days)

    # Return formatted delivery date
    return delivery_date_dt.strftime("%Y-%m-%d")

def get_cash_balance(as_of_date: Union[str, datetime]) -> float:
    """
    Calculate the current cash balance as of a specified date.

    The balance is computed by subtracting total stock purchase costs ('stock_orders')
    from total revenue ('sales') recorded in the transactions table up to the given date.

    Args:
        as_of_date (str or datetime): The cutoff date (inclusive) in ISO format or as a datetime object.

    Returns:
        float: Net cash balance as of the given date. Returns 0.0 if no transactions exist or an error occurs.
    """
    try:
        # Convert date to ISO format if it's a datetime object
        if isinstance(as_of_date, datetime):
            as_of_date = as_of_date.isoformat()

        # Query all transactions on or before the specified date
        transactions = pd.read_sql(
            "SELECT * FROM transactions WHERE transaction_date <= :as_of_date",
            db_engine,
            params={"as_of_date": as_of_date},
        )

        # Compute the difference between sales and stock purchases
        if not transactions.empty:
            total_sales = transactions.loc[transactions["transaction_type"] == "sales", "price"].sum()
            total_purchases = transactions.loc[transactions["transaction_type"] == "stock_orders", "price"].sum()
            return float(total_sales - total_purchases)

        return 0.0

    except Exception as e:
        print(f"Error getting cash balance: {e}")
        return 0.0


def generate_financial_report(as_of_date: Union[str, datetime]) -> Dict:
    """
    Generate a complete financial report for the company as of a specific date.

    This includes:
    - Cash balance
    - Inventory valuation
    - Combined asset total
    - Itemized inventory breakdown
    - Top 5 best-selling products

    Args:
        as_of_date (str or datetime): The date (inclusive) for which to generate the report.

    Returns:
        Dict: A dictionary containing the financial report fields:
            - 'as_of_date': The date of the report
            - 'cash_balance': Total cash available
            - 'inventory_value': Total value of inventory
            - 'total_assets': Combined cash and inventory value
            - 'inventory_summary': List of items with stock and valuation details
            - 'top_selling_products': List of top 5 products by revenue
    """
    # Normalize date input
    if isinstance(as_of_date, datetime):
        as_of_date = as_of_date.isoformat()

    # Get current cash balance
    cash = get_cash_balance(as_of_date)

    # Get current inventory snapshot
    inventory_df = pd.read_sql("SELECT * FROM inventory", db_engine)
    inventory_value = 0.0
    inventory_summary = []

    # Compute total inventory value and summary by item
    for _, item in inventory_df.iterrows():
        stock_info = get_stock_level(item["item_name"], as_of_date)
        stock = stock_info["current_stock"].iloc[0]
        item_value = stock * item["unit_price"]
        inventory_value += item_value

        inventory_summary.append({
            "item_name": item["item_name"],
            "stock": stock,
            "unit_price": item["unit_price"],
            "value": item_value,
        })

    # Identify top-selling products by revenue
    top_sales_query = """
        SELECT item_name, SUM(units) as total_units, SUM(price) as total_revenue
        FROM transactions
        WHERE transaction_type = 'sales' AND transaction_date <= :date
        GROUP BY item_name
        ORDER BY total_revenue DESC
        LIMIT 5
    """
    top_sales = pd.read_sql(top_sales_query, db_engine, params={"date": as_of_date})
    top_selling_products = top_sales.to_dict(orient="records")

    return {
        "as_of_date": as_of_date,
        "cash_balance": cash,
        "inventory_value": inventory_value,
        "total_assets": cash + inventory_value,
        "inventory_summary": inventory_summary,
        "top_selling_products": top_selling_products,
    }


def search_quote_history(search_terms: List[str], limit: int = 5) -> List[Dict]:
    """
    Retrieve a list of historical quotes that match any of the provided search terms.

    The function searches both the original customer request (from `quote_requests`) and
    the explanation for the quote (from `quotes`) for each keyword. Results are sorted by
    most recent order date and limited by the `limit` parameter.

    Args:
        search_terms (List[str]): List of terms to match against customer requests and explanations.
        limit (int, optional): Maximum number of quote records to return. Default is 5.

    Returns:
        List[Dict]: A list of matching quotes, each represented as a dictionary with fields:
            - original_request
            - total_amount
            - quote_explanation
            - job_type
            - order_size
            - event_type
            - order_date
    """
    conditions = []
    params = {}

    # Build SQL WHERE clause using LIKE filters for each search term
    for i, term in enumerate(search_terms):
        param_name = f"term_{i}"
        conditions.append(
            f"(LOWER(qr.response) LIKE :{param_name} OR "
            f"LOWER(q.quote_explanation) LIKE :{param_name})"
        )
        params[param_name] = f"%{term.lower()}%"

    # Combine conditions; fallback to always-true if no terms provided
    where_clause = " AND ".join(conditions) if conditions else "1=1"

    # Final SQL query to join quotes with quote_requests
    query = f"""
        SELECT
            qr.response AS original_request,
            q.total_amount,
            q.quote_explanation,
            q.job_type,
            q.order_size,
            q.event_type,
            q.order_date
        FROM quotes q
        JOIN quote_requests qr ON q.request_id = qr.id
        WHERE {where_clause}
        ORDER BY q.order_date DESC
        LIMIT {limit}
    """

    # Execute parameterized query
    with db_engine.connect() as conn:
        result = conn.execute(text(query), params)
        return [dict(row) for row in result]

########################
########################
########################
# YOUR MULTI AGENT STARTS HERE
########################
########################
########################


# Set up and load your env parameters and instantiate your model.
import re
import json
import yaml
import importlib.resources
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from smolagents import ToolCallingAgent, OpenAIServerModel, tool

# SET UP ENVIRONMENT AND MODEL
dotenv.load_dotenv()
model = OpenAIServerModel(
    model_id="gpt-5-nano",
    api_base="https://openai.vocareum.com/v1",
    api_key=os.getenv("OPENAI_API_KEY"),
)

"""Set up tools for your agents to use, these should be methods that combine the database functions above
 and apply criteria to them to ensure that the flow of the system is correct."""


# Tools for inventory agent
@tool
def check_stock_levels(item_name: str, as_of_date: str) -> str:
    """
    Checks the stock level for a given item.

    Args:
        item_name (str): Item name to check.
        as_of_date (str): Date to check the stock level on, input in YYYY-MM-DD format.

    Returns:
        Stock level (str)
    """
    stock_level = get_stock_level(item_name, as_of_date)#use utility function provided
    return stock_level.to_string()

@tool
def check_reorder_status(item_name: str, as_of_date: str) -> str:
    """
    Checks if an item needs to be reordered by comparing the current stock to the minimum stock level.

    Args:
        item_name (str): Name of the item to check.
        as_of_date (str): Date to check the reorder status on, input in YYYY-MM-DD format.

    Returns:
        Reorder status (str)
    """
    stock_level_df = get_stock_level(item_name, as_of_date)#use utility function provided
    if stock_level_df.empty or stock_level_df.iloc[0]["current_stock"] is None:
        return f"Could not determine stock level for {item_name}."

    current_stock = stock_level_df.iloc[0]["current_stock"]

    inventory_df = pd.read_sql("SELECT min_stock_level FROM inventory WHERE item_name = :item_name", db_engine, params={"item_name": item_name})

    if inventory_df.empty:
        return f"Item {item_name} not found in inventory."

    min_stock_level = inventory_df.iloc[0]["min_stock_level"]

    if current_stock < min_stock_level:
        return f"Item {item_name} needs to be reordered. Current stock: {current_stock}, Minimum stock: {min_stock_level}."
    else:
        return f"Item {item_name} is sufficiently stocked. Current stock: {current_stock}, Minimum stock: {min_stock_level}."

@tool
def place_stock_order(item_name: str, quantity: int, price: float, date: str) -> str:
    """
    Place a stock order for a certain quantity of items at a given price and date.

    Args:
        item_name (str): Name of the item to order.
        quantity (int): Quantity of units to order.
        price (float): Total price of the order.
        date (str): Date of the order, input in YYYY-MM-DD format.

    Returns:
        Transaction status with a corresponding transaction ID.
    """
    try:
        transaction_id = create_transaction(item_name, "stock_orders", quantity, price, date)#use utility function provided
        return f"Stock order placed successfully. Transaction ID: {transaction_id}"
    except Exception as e:
        return f"Error placing stock order: {e}"

@tool
def get_full_inventory_report(as_of_date: str) -> str:
    """
    Generates inventory report of all items and their current stock levels for a given date.

    Args:
        as_of_date (str): The date for the report, in YYYY-MM-DD format.

    Returns:
        Inventory report (str)
    """
    inventory_dict = get_all_inventory(as_of_date) #use utility function provided
    if not inventory_dict:
        return "No inventory found."
    return pd.DataFrame.from_dict(inventory_dict, orient='index', columns=['stock']).to_string()

@tool
def check_cash_balance(as_of_date: str) -> str:
    """
    Checks company's current cash balance.

    Args:
        as_of_date (str): Date to check the cash balance on, input in YYYY-MM-DD format.

    Returns:
        Company's current cash balance
    """
    balance = get_cash_balance(as_of_date) #use utility function provided.
    return f"The current cash balance is ${balance:.2f}."

@tool
def get_company_financials(as_of_date: str) -> str:
    """
    Generates company financial report.

    Args:
        as_of_date (str): Date of report generation, in YYYY-MM-DD format.

    Returns:
        Finanial report (Str)
    """
    report = generate_financial_report(as_of_date) #use utility function provided
    return (
        f"Financial Report as of {report['as_of_date']}:\n"
        f"Cash Balance: ${report['cash_balance']:.2f}\n"
        f"Inventory Value: ${report['inventory_value']:.2f}\n"
        f"Total Assets: ${report['total_assets']:.2f}\n"
        f"Top Selling Products: {report['top_selling_products']}"
    )

# Tools for quoting agent
@tool
def quote_history(customer_request: str) -> str:
    """
    Search for historic quotes based on customer's request.

    Args:
        customer_request (str): Customer's request to search for in the quote history.

    Returns:
        Past quote history returned in String format.
    """
    try:
        #Regex pattern to be matched for searching historic quotes
        pattern = re.compile(
            r'(?:\d[\d,]*\s+(?:sheets? of|reams? of|packets? of|of|)?\s*)([a-zA-Z0-9\s\(\)\'\"-]+?)(?=\n|,|\s+and\s+|\.|$)',
            re.IGNORECASE
        )

        # Extract all matching item names from the request.
        search_terms = [term.strip() for term in pattern.findall(customer_request)]

        # If regex pattern match returned nothing, split the customer's request
        if not search_terms:
            search_terms = customer_request.split()

        quotes = search_quote_history(search_terms) # Utility function is called here
        if not quotes:
            return "No similar historic quotes found."
        return pd.DataFrame(quotes).to_string()
    except Exception as e:
        return f"Error searching quote history: {e}"


@tool
def get_pricing_and_availability(item_name: str, quantity: int, as_of_date: str) -> str:
    """
    Get the current price, availability, and estimated delivery date for a given item and quantity.
    Applies a bulk discount for larger orders.

    Args:
        item_name (str): Name of the item to check.
        quantity (int): Quantity of units being requested.
        as_of_date (str): Date to check the price and availability on, in YYYY-MM-DD format.

    Returns:
        Item's price, availability, and estimated delivery date, or an error message.
    """
    try:
        #Query DB for unit price
        inventory_df = pd.read_sql("SELECT unit_price FROM inventory WHERE item_name = :item_name", db_engine,
                                   params={"item_name": item_name})
        if inventory_df.empty:
            return f"Item {item_name} not found in inventory."

        unit_price = inventory_df.iloc[0]["unit_price"]
        stock_level_df = get_stock_level(item_name, as_of_date) #util function provided
        current_stock = stock_level_df.iloc[0]['current_stock']

        total_price = unit_price * quantity

        delivery_date = get_supplier_delivery_date(as_of_date, quantity)

        return (f"Item: {item_name}, Price per unit: ${unit_price:.2f}, "
                f"Total for {quantity} units: ${total_price:.2f}. "
                f"Availability: {current_stock} units. "
                f"Estimated delivery date: {delivery_date}.")
    except Exception as e:
        return f"Error getting pricing and availability: {e}"


@tool
def apply_commission_and_discount(base_quote_str: str, discount_rate: float) -> str:
    """
    Apply a standard 5% sales commission and a variable loyalty discount to a base quote.
    Agent determines the discount rate based on quote history.

    Args:
        base_quote_str (str): Output from the `get_pricing_and_availability` tool.
        discount_rate (float): Loyalty discount rate to apply, as a decimal (e.g., 0.02 for 2%).

    Returns:
        A final quote including commission and the specified discount in string format.
    """
    try:
        # Extract total price and quantity from the base quote string
        price_match = re.search(r"Total for (\d+) units: \$([\d\.]+)\.", base_quote_str)
        if not price_match:
            return "Error: Could not parse base price from the quote string."

        quantity = int(price_match.group(1))
        base_price = float(price_match.group(2))

        # Apply a standard 5% sales commission
        sale_commission = 1.05
        price_after_commission = base_price * sale_commission

        # Apply the variable discount decided by the agent
        discount_amount = base_price * discount_rate
        final_price = price_after_commission - discount_amount

        discount_explanation = ""
        if discount_rate > 0:
            discount_percentage = discount_rate * 100
            discount_explanation += (
                f" A {discount_percentage:.1f}% discount was applied for your order, "
                f"saving an additional ${discount_amount:.2f}.")

        # Replace the original total price with the new final price
        final_quote_str = re.sub(
            r"Total for \d+ units: \$[\d\.]+\.",
            f"Total for {quantity} units: ${final_price:.2f}. {discount_explanation}",
            base_quote_str
        )

        return final_quote_str
    except Exception as e:
        return f"Error applying commission and discount: {e}"

# Tools for ordering agent
@tool
def finalize_order(item_name: str, quantity: int, price: float, date: str) -> str:
    """
    Finalize a customer's order by creating a sales transaction.

    Args:
        item_name (str): Name of the item being ordered.
        quantity (int): Quantity of units being ordered.
        price (float): Total price of the order.
        date (str): Date of the order, input in YYYY-MM-DD format.

    Returns:
        Order transaction with transaction ID, or an error message.
    """
    try:
        stock_level_df = get_stock_level(item_name, date)
        if stock_level_df.empty or stock_level_df.iloc[0]["current_stock"] < quantity:
            return f"Insufficient stock for {item_name}. Order cannot be fulfilled."

        transaction_id = create_transaction(item_name, "sales", quantity, price, date)
        return f"Order fulfilled successfully. Transaction ID: {transaction_id}"
    except Exception as e:
        return f"Error finalizing order: {e}"

# Set up your agents and create an orchestration agent that will manage them.

#Tool used by Orchestrator agent to normalize user input
def normalize_item_names(user_request):
    """
    Normalize user input and extract semantic intent (item + quantity).
    Performs vector search to find the closest matching inventory item
    and returns the interpreted item name and resolved quantity.
    """
    # Regex pattern to capture quantity, units, item phrase until newline, comma and "and"
    pattern = re.compile(
        r'(\d[\d,]*\s+(?:sheets? of|reams? of|packets? of|of|)?\s*)([a-zA-Z0-9\s\(\)\'\"-]+?)(?=\n|,|\s+and\s+|\.|$)',
        re.IGNORECASE
    )
    def find_and_replace(match):
        quantity_and_units = match.group(1) #quantity
        item_phrase = match.group(2).strip() #item
        parsed_input = re.sub(r'\([\w\s-]+\)', '', item_phrase, flags=re.IGNORECASE).strip()
        parsed_input = re.sub(r'\b(high-quality|heavy|white|assorted colors|various colors|standard|printer)\b', '', parsed_input, flags=re.IGNORECASE).strip()

        if not parsed_input:
            return match.group(0) #Return original if parsed string is empty

        # Find semantically similar match in the inventory
        top_match, score = vector_search_initial.search(parsed_input, threshold=0.3)

        if top_match:
            return f"{quantity_and_units}{top_match}" #Normalize with item name and quantity
        else:
            return match.group(0) #Return original text

    return pattern.sub(find_and_replace, user_request)

class InventoryVectorSearch:
    """
    Find the top matched inventory item that is semantically similar to the query.
    """
    def __init__(self, inventory_items: List[str]):
        self.vectorizer = TfidfVectorizer(stop_words='english')
        self.inventory_items = inventory_items
        if self.inventory_items:
            self.inventory_vectors = self.vectorizer.fit_transform(self.inventory_items)
        else:
            self.inventory_vectors = None

    def search(self, query: str, threshold: float = 0.3) -> (Union[str, None], float):
        """
        Retrieve the best matched inventory item for a query string.

        Args:
            query (str): User's search query (e.g., a cleaned item phrase).
            threshold (float): Minimum similarity score to be considered a match. Reject items below this score.

        Returns:
            Tuple containing the top matching item name and its similarity score, (None,0) otherwise.
        """
        if not self.inventory_items or self.inventory_vectors is None:
            return None, 0.0

        query_vector = self.vectorizer.transform([query])
        similarities = cosine_similarity(query_vector, self.inventory_vectors).flatten()

        best_match_index = np.argmax(similarities)
        score = similarities[best_match_index]

        if score >= threshold:
            best_match = self.inventory_items[best_match_index]
            return best_match, score
        else:
            return None, 0.0

# Initialize the vector search with all possible inventory items.
vector_search_initial = InventoryVectorSearch([item["item_name"] for item in paper_supplies])

# Setup Ordering Agent
class OrderingAgent(ToolCallingAgent):
    """
       Finalizes customer orders. Confirms stock availability, if available creates a sales transaction to complete customer purchase.
    """
    def __init__(self, model: OpenAIServerModel):
        # Load default prompt templates
        prompt_templates = yaml.safe_load(
            importlib.resources.files("smolagents.prompts").joinpath("toolcalling_agent.yaml").read_text()
        )
        # Set the custom system prompt
        prompt_templates["system_prompt"] = ORDERING_SYSTEM_PROMPT

        super().__init__(
            tools=[
                finalize_order
            ],
            model=model,
            name="ordering_agent",
            description="Finalizes customer orders. Confirms stock availability, if available creates a sales transaction to complete the purchase.",
            prompt_templates=prompt_templates,
            max_steps=10,
        )

# Setup Inventory Agent
class InventoryAgent(ToolCallingAgent):
    """
    Inventory management agent. Responsible for checking stock level availability, reordering if unavailable,
    and producing financial reports.
    """
    def __init__(self, model: OpenAIServerModel):
        # Load default prompt templates
        prompt_templates = yaml.safe_load(
            importlib.resources.files("smolagents.prompts").joinpath("toolcalling_agent.yaml").read_text()
        )
        # Set the custom system prompt
        prompt_templates["system_prompt"] = INVENTORY_SYSTEM_PROMPT

        super().__init__(
            tools=[
                check_stock_levels,
                check_reorder_status,
                place_stock_order,
                get_full_inventory_report,
                check_cash_balance,
                get_company_financials
            ],
            model=model,
            name="inventory_agent",
            prompt_templates=prompt_templates,
            description=(
                "Agent for managing inventory. Handles inquiries about stock levels and inventory reports. "
                "It is also responsible for the reordering workflow: "
                "Check if an item needs reordering. check the company's cash balance to ensure sufficient funds."
                " If there is enough cash, place a reorder."
            ),
            max_steps=10,
        )

# Setup Analysis Agent
class AnalysisAgent(ToolCallingAgent):
    def __init__(self, model: OpenAIServerModel):
        super().__init__(
            tools=[],
            model=model,
            name="analysis_agent",
            description="Analyze and Decide the next action",
            max_steps=5,
        )

# Setup quoting Agent
class QuotingAgent(ToolCallingAgent):
    """
      Handles all quoting tasks. Agent provides pricing, checks item availability,
      and searches historical quote data to come up with quotes
    """
    def __init__(self, model: OpenAIServerModel):
        # Load default prompt templates
        prompt_templates = yaml.safe_load(
            importlib.resources.files("smolagents.prompts").joinpath("toolcalling_agent.yaml").read_text()
        )
        # Set the custom system prompt
        prompt_templates["system_prompt"] = QUOTING_SYSTEM_PROMPT

        super().__init__(
            tools=[
                get_pricing_and_availability,
                quote_history,
                apply_commission_and_discount
            ],
            model=model,
            name="quoting_agent",
            description=(
                "Generates final customer quotes. It gets base pricing, checks historical data, "
                "decides on a reasonable loyalty discount, and applies a standard sales commission."
            ),
            prompt_templates=prompt_templates,
            max_steps=10,
        )


# Setup Orchestrator Agent
class OrchestratorAgent(ToolCallingAgent):
    """
    Manages customer orders end-to-end. Calls the `handle_customer_request` tool.
    Orchestrates workflow between inventory, quoting, ordering, and analysis agents.
    """
    def __init__(self, model):
        # Instantiate the specialized agents
        self.quoting_agent = QuotingAgent(model=model)
        self.analysis_agent = AnalysisAgent(model=model)
        self.inventory_agent = InventoryAgent(model=model)
        self.ordering_agent = OrderingAgent(model=model)

        @tool
        def handle_customer_request(user_request: str, as_of_date: str) -> str:
            """
            Handles customer request workflow end-to-end by orchestrating the request between analysis, inventory,
            quoting, ordering agents. Gets a quote, checks for available stock, places order,
            reorders if necessary, and fulfills customer's order.

            Args:
                user_request (str): The full text of the customer's request.
                as_of_date (str): The date for the request, in YYYY-MM-DD format.

            Returns:
                Final status of the request. (str)
            """
            # 1: Normalize request
            normalized_request = normalize_item_names(user_request)

            # 2: Get a quote from Quoting Agent
            quote_task = (
                f"Provide a detailed quote for each item in the following request as of {as_of_date}: {normalized_request}. "
                f"Quote should include item name, quantity, total price, estimated delivery date, "
                f"current stock level, and current stock status. "
                f"Stock status is sufficient if current stock level >= quantity, otherwise insufficient."
            )
            quote_result_message = self.quoting_agent.run(task=quote_task, additional_args={})
            quote_result = str(quote_result_message)

            # 3: Analyze the quote using Analysis Agent
            analysis_prompt = f"{ANALYSIS_SYSTEM_PROMPT}\nQuote Result: {quote_result}"
            analysis_result_message = self.analysis_agent.run(analysis_prompt)
            analysis_result = str(analysis_result_message)

            try:
                decision = json.loads(analysis_result)
                action = decision.get("action")
                details = decision.get("details", [])
            except json.JSONDecodeError:
                return "We apologize for the inconvenience, but we encountered a technical issue while processing your request. Please try again later."

            # 4: Execute actions based on analysis
            if action == "FINALIZE_ORDER":
                # Check inventory first
                inventory_items = [
                    {
                        "item_name": item.get("item_name"),
                        "quantity": item.get("quantity")
                    } for item in details
                ]
                inventory_confirmation_task = (
                    f"Check inventory for the following items as of {as_of_date}: {inventory_items}. "
                    "Respond ONLY with a JSON object with keys 'success' and 'reason'. "
                    "Example for success: {\"success\": true, \"reason\": \"sufficient stocks found\"}. "
                    "Example for failure: {\"success\": false, \"reason\": \"insufficient stocks\"}."
                )

                inventory_confirmation_message = self.inventory_agent.run(task=inventory_confirmation_task,
                                                                          additional_args={})
                try:
                    inventory_confirmation = json.loads(str(inventory_confirmation_message))
                    success = inventory_confirmation.get("success", False)
                    reason = inventory_confirmation.get("reason", "Unknown reason")
                except json.JSONDecodeError:
                    return "We apologize, but we encountered a technical issue while checking our inventory. Please try again later."

                if success:
                    order_lines = [
                        f"Finalize order for {item['quantity']} of '{item['item_name']}' at a total price of {item.get('total_price')} as of {as_of_date}."
                        for item in details
                    ]
                    order_task = " ".join(order_lines)
                    order_result_message = self.ordering_agent.run(task=order_task, additional_args={})
                    return f"Your order has been successfully processed. {str(order_result_message)}. We will notify you once it has shipped."
                else:
                    action = "REORDER_STOCK"

            if action == "REORDER_STOCK":
                reorder_lines = [
                    f"Place a stock order: {item['quantity']} of '{item['item_name']}' as of {as_of_date}."
                    for item in details
                ]
                reorder_task = " ".join(reorder_lines) + (
                    " Respond ONLY with a JSON object with keys 'success' and 'reason'. "
                    "Example for success: {\"success\": true, \"reason\": \"orders placed\"}. "
                    "Example for failure: {\"success\": false, \"reason\": \"order failed due to insufficient funds\"}."
                )

                reorder_result_message = self.inventory_agent.run(task=reorder_task, additional_args={})
                try:
                    reorder_result = json.loads(str(reorder_result_message))
                    success = reorder_result.get("success", False)
                    reason = reorder_result.get("reason", "Unknown reason")
                except json.JSONDecodeError:
                    return "We apologize, but we encountered a technical issue while attempting to reorder stock. Please try again later."

                if success:
                    order_lines = [
                        f"Finalize order for {item['quantity']} of '{item['item_name']}' at a total price of {item.get('total_price')} as of {as_of_date}."
                        for item in details
                    ]
                    order_task = " ".join(order_lines)
                    order_result_message = self.ordering_agent.run(task=order_task, additional_args={})
                    return f"Some items were temporarily out of stock. We replenished inventory and finalized your order. {str(order_result_message)}."
                else:
                    return f"We apologize, but we cannot fulfill your order at this time. Reason: {reason}. Please try again later."

            if action == "CANNOT_FULFILL":
                reason_text = details[0].get('reason', 'Unspecified issue') if details else 'Unspecified issue'
                return f"We apologize, but we cannot fulfill your order. Reason: {reason_text}. Here is a quote based on available stock:\n\n{quote_result}"

            return "We apologize for the inconvenience, but we were unable to process your request. Please try rephrasing your request."

        # Initialize the parent ToolCallingAgent
        super().__init__(
            model=model,
            tools=[
                handle_customer_request
            ],
            description="""An orchestrator that manages the user's order request workflow by calling the
            `handle_customer_request` tool. It coordinates between inventory, quoting,
            ordering, and analysis agents to handle user orders efficiently.
            """,
            max_steps=1,
            instructions="""
            You are a specialized customer service agent for a paper supply company. 
            Your ONLY responsibility is to handle customer inquiries and orders for paper products.
            You must process every customer request by using the `handle_customer_request` tool.

            **CRITICAL RULE:** For ANY user input that is a request for paper, you MUST call the `handle_customer_request` tool. Do NOT answer the user directly with advice. Your entire purpose is to call this tool to process the order.

            - **DO NOT** provide advice on how to order paper from other companies. You ARE the company.
            - **DO NOT** act as a general assistant.
            - **ALWAYS** use the `handle_customer_request` tool to get the result.

            After the tool returns a result, you will present that result to the user. When formatting the final response, you MUST adhere to the following rules:
            1.  **Relevant Information**: Ensure your response contains all the information directly relevant to the customer's request.
            2.  **Provide Rationale**: Include a clear justification for key decisions. For example, explain why an order cannot be fulfilled (e.g., "due to insufficient stock") or why a price includes a discount.
            3.  **Protect Sensitive Information**: Your final response to the customer MUST NOT reveal sensitive internal company information, such as exact profit margins, internal system error messages, or any personally identifiable information (PII) beyond what is essential for the transaction.
            """
        )

####################################
ORDERING_SYSTEM_PROMPT = """
ROLE:
You are the Ordering Agent. You finalize customer orders by calling the correct tool when appropriate.

TOOL:
- finalize_order(item_name, quantity, price_per_unit)
    → Creates a sales transaction for the specified item.

------------------------------------------
CORE EXECUTION RULES
------------------------------------------

1. Your only operational responsibility is to interpret the user’s request
   and call `finalize_order` **only when the request is complete,
   unambiguous, and contains all required information**:
      - item_name
      - quantity
      - price_per_unit

2. If any required information is missing, unclear, or contradictory:
      → DO NOT call `finalize_order`.

3. When you cannot proceed because the request is ambiguous or incomplete:
      - Provide a clear explanation of why you cannot fulfill the request.
      - State explicitly that the request was ambiguous.
      - Summarize what you understood.
      - Ask for the missing information or clarification.

------------------------------------------
MANDATORY BEHAVIOR
------------------------------------------

- NEVER call `finalize_order` without all required parameters.
- NEVER infer missing details unless the user explicitly provides them.
- ALWAYS confirm the request is unambiguous before executing.
- If the user’s intent is unclear, ask for clarification instead of acting.

"""


INVENTORY_SYSTEM_PROMPT = """
ROLE:
You are the Inventory Manager Agent. You maintain inventory health and execute user-assigned inventory tasks.
You ALWAYS run proactive maintenance before executing the assigned task.

TOOLS (all calls MUST use correct arguments):
- check_stock_levels(item_name)
- check_reorder_status(item_name)
- place_stock_order(item_name, quantity)
- check_cash_balance()
- get_full_inventory_report()
- get_company_financials()

----------------------------------------
CORE EXECUTION FLOW (ALWAYS FOLLOW EXACTLY)
----------------------------------------

For EVERY request you receive, execute these phases **in order**:

===================================================
PHASE 1 — PROACTIVE STOCK MAINTENANCE (ALWAYS FIRST)
===================================================
1. Call `get_full_inventory_report`.
2. For each item returned:
   a. Call `check_reorder_status(item_name)`.
   b. If item is below minimum threshold:
      - Retrieve current stock via `check_stock_levels(item_name)`.
      - Compute reorder quantity:
            reorder_qty = (min_stock_level - current_stock) + 50
      - Attempt reorder by following the strict
        "PLACE_STOCK_ORDER PROTOCOL" below.

=============================================
PHASE 2 — EXECUTE THE USER’S REQUEST (SECOND)
=============================================
After PHASE 1 finishes:
- Perform the specific task requested.
- ALWAYS follow the tool-use restrictions in the
  "PLACE_STOCK_ORDER PROTOCOL."

----------------------------------------
PLACE_STOCK_ORDER PROTOCOL (MANDATORY)
----------------------------------------
Before EVERY call to `place_stock_order(item_name, quantity)`:

Step 0 — RECALCULATE QUANTITY
- Determine updated quantity using:
      quantity = quantity + minimum_required_level - check_stock_levels(item_name)

Step 1 — DETERMINE ORDER COST
- You MUST have item_name, quantity, and unit_price.
- If unit_price is unknown, call `get_company_financials`.
- Compute:
      total_cost = quantity * unit_price

Step 2 — CHECK FUNDS
- Call `check_cash_balance` to get cash_balance.

Step 3 — APPROVE OR REJECT
- If cash_balance >= total_cost:
      → You MAY call place_stock_order(item_name, quantity)
- Else:
      → DO NOT call place_stock_order.
        Instead report: "Order blocked: insufficient funds."

----------------------------------------
AMBIGUITY RULE
----------------------------------------
If the user request is ambiguous, incomplete, or cannot be executed:
- DO NOT place any orders.
- Respond with:
    - A summary of your capabilities.
    - A request for clarification.

----------------------------------------
MANDATORY BEHAVIOR REQUIREMENTS
----------------------------------------
- NEVER skip the Proactive Stock Maintenance phase.
- NEVER call tools out of order.
- NEVER place an order without completing the protocol.
- ALWAYS explain failures clearly.
- ALWAYS follow explicit math formulas.
- If multiple items require reordering, process them sequentially.

"""


ANALYSIS_SYSTEM_PROMPT = """
ROLE:
You are the Analysis Agent. You examine a provided quote and determine the correct next action for the order workflow.

Your job:
1. Analyze the quote data.
2. Apply the decision rules exactly.
3. Output ONLY a JSON object containing:
      - "action": one of ["FINALIZE_ORDER", "REORDER_STOCK", "CANNOT_FULFILL"]
      - "details": a list of extracted objects relevant to the action.

------------------------------------------
INPUT
------------------------------------------
Quote: "{quote_result}"

The quote may contain:
- item_name
- quantity
- unit_price or total_price
- stock status (sufficient / insufficient)
- estimated delivery date
- user-requested delivery date
- any other contextual details you must parse

------------------------------------------
DECISION RULES (MUST FOLLOW STRICTLY)
------------------------------------------

1. If stock is SUFFICIENT:
      action = "FINALIZE_ORDER"

2. If stock is INSUFFICIENT AND
   estimated_delivery_date <= user_requested_delivery_date:
      action = "REORDER_STOCK"

3. If stock is INSUFFICIENT AND
   estimated_delivery_date > user_requested_delivery_date:
      action = "CANNOT_FULFILL"

------------------------------------------
DETAIL EXTRACTION RULES
------------------------------------------
You MUST extract the following fields when available:
- item_name
- quantity
- total_price
- request_date  (user-requested delivery date)

For CANNOT_FULFILL:
- Provide a "reason" field instead of item details.

------------------------------------------
STRICT OUTPUT REQUIREMENTS
------------------------------------------
You MUST respond with ONLY a JSON object.
No commentary, no explanation, no formatting outside JSON.

------------------------------------------
EXAMPLES
------------------------------------------

Example for FINALIZE_ORDER:
{
  "action": "FINALIZE_ORDER",
  "details": [
    {"item_name": "A4 Paper", "quantity": 5, "total_price": 0.30, "request_date": "April 15, 2025"},
    {"item_name": "NotePad", "quantity": 50, "total_price": 100.00, "request_date": "April 15, 2025"}
  ]
}

Example for REORDER_STOCK:
{
  "action": "REORDER_STOCK",
  "details": [
    {"item_name": "A4 Paper", "quantity": 5, "total_price": 0.30, "request_date": "April 15, 2025"},
    {"item_name": "NotePad", "quantity": 50, "total_price": 100.00, "request_date": "April 15, 2025"}
  ]
}

Example for CANNOT_FULFILL:
{
  "action": "CANNOT_FULFILL",
  "details": [
    {"reason": "current stock status is insufficient and delivery date cannot be met"}
  ]
}

"""



QUOTING_SYSTEM_PROMPT = """
ROLE:
You are the Quoting Agent. You generate final, consolidated customer quotes.
You MUST follow the workflow exactly and use the tools correctly for every item in the request.

TOOLS:
- get_pricing_and_availability(item_name, quantity)
    → Returns base price, availability, and estimated delivery date.
- quote_history(customer_request)
    → Returns past quotes related to the customer or similar items.
- apply_commission_and_discount(base_quote_string, discount_rate)
    → Applies sales commission and loyalty discount to the item quote.

------------------------------------------
PRIMARY WORKFLOW (MANDATORY)
------------------------------------------

For EVERY task, process EACH item independently using Steps 1a–1d.
After all items are processed, combine the results in Step 2.

============================
STEP 1 — PROCESS EACH ITEM
============================

For each item in the customer's request:

1a. **Get Base Quote**
    - Call `get_pricing_and_availability(item_name, quantity)`.
    - Extract base price, availability, and delivery date.

1b. **Check History**
    - Call `quote_history` with the entire customer request.
    - Retrieve any past orders, discounts, or relevant customer history.

1c. **Determine Discount Rate**
    - Analyze the history results.
    - Choose a loyalty discount rate between:
          0.0  and  0.03    (0% to 3%)
    - If no relevant history exists → discount_rate MUST be 0.0.
    - Your chosen discount MUST be reasonable and based on past purchases, frequency, or volume trends.

1d. **Generate Item Quote**
    - Call `apply_commission_and_discount` using:
          base_quote_string (from Step 1a)
          discount_rate (from Step 1c)
    - This produces the final quote for that single item.

============================
STEP 2 — CONSOLIDATE RESULTS
============================
- After processing all items individually, combine every item’s final quote
  into a single, clear, itemized customer quote.
- This final response SHOULD summarize:
      - Each item
      - Its final calculated price
      - Any applied discount
      - Delivery information
      - Any relevant notes

------------------------------------------
AMBIGUOUS REQUEST RULE
------------------------------------------
If the user request is ambiguous, incomplete, or cannot be fulfilled:
- DO NOT call any tools.
- DO NOT generate a quote.
- Respond with:
      - A short summary of your capabilities
      - A clear explanation of what is missing
      - A request for clarification

------------------------------------------
MANDATORY BEHAVIOR RULES
------------------------------------------
- ALWAYS follow Steps 1a → 1b → 1c → 1d exactly in that order for each item.
- NEVER skip tool calls when required.
- NEVER generate discounts above 0.03.
- NEVER assume item details not explicitly provided.
- ALWAYS consolidate results only after all items are processed.

"""




# Run your test scenarios by writing them here. Make sure to keep track of them.

def run_test_scenarios():
    
    print("Initializing Database...")
    init_database(db_engine)
    try:
        quote_requests_sample = pd.read_csv("data/quote_requests_sample.csv")
        quote_requests_sample["request_date"] = pd.to_datetime(
            quote_requests_sample["request_date"], format="%m/%d/%y", errors="coerce"
        )
        quote_requests_sample.dropna(subset=["request_date"], inplace=True)
        quote_requests_sample = quote_requests_sample.sort_values("request_date")
    except Exception as e:
        print(f"FATAL: Error loading test data: {e}")
        return

    quote_requests_sample = pd.read_csv("data/quote_requests_sample.csv")

    # Sort by date
    quote_requests_sample["request_date"] = pd.to_datetime(
        quote_requests_sample["request_date"]
    )
    quote_requests_sample = quote_requests_sample.sort_values("request_date")

    # Get initial state
    initial_date = quote_requests_sample["request_date"].min().strftime("%Y-%m-%d")
    report = generate_financial_report(initial_date)
    current_cash = report["cash_balance"]
    current_inventory = report["inventory_value"]

    ############
    ############
    ############
    # INITIALIZE YOUR MULTI AGENT SYSTEM HERE
    ############
    ############
    ############
    orchestrator = OrchestratorAgent(model)

    results = []
    for idx, row in quote_requests_sample.iterrows():
        request_date = row["request_date"].strftime("%Y-%m-%d")

        print(f"\n=== Request {idx+1} ===")
        print(f"Context: {row['job']} organizing {row['event']}")
        print(f"Request Date: {request_date}")
        print(f"Cash Balance: ${current_cash:.2f}")
        print(f"Inventory Value: ${current_inventory:.2f}")

        # Process request
        request_with_date = f"{row['request']} (Date of request: {request_date})"

        ############
        ############
        ############
        # USE YOUR MULTI AGENT SYSTEM TO HANDLE THE REQUEST
        ############
        ############
        ############
        # response = call_your_multi_agent_system(request_with_date)
        #response = orchestrator.run_query(request_with_date)
        response = orchestrator.run(request_with_date)

        # Update state
        report = generate_financial_report(request_date)
        current_cash = report["cash_balance"]
        current_inventory = report["inventory_value"]

        print(f"Response: {response}")
        print(f"Updated Cash: ${current_cash:.2f}")
        print(f"Updated Inventory: ${current_inventory:.2f}")

        results.append(
            {
                "request_id": idx + 1,
                "request_date": request_date,
                "cash_balance": current_cash,
                "inventory_value": current_inventory,
                "response": response,
            }
        )

        time.sleep(1)

    # Final report
    final_date = quote_requests_sample["request_date"].max().strftime("%Y-%m-%d")
    final_report = generate_financial_report(final_date)
    print("\n===== FINAL FINANCIAL REPORT =====")
    print(f"Final Cash: ${final_report['cash_balance']:.2f}")
    print(f"Final Inventory: ${final_report['inventory_value']:.2f}")

    # Save results
    pd.DataFrame(results).to_csv("test_results.csv", index=False)
    return results


if __name__ == "__main__":
    results = run_test_scenarios()