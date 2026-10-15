"""A deliberately imperfect demo application for SonarQube practice.

This file is self-contained and uses only the Python standard library.
Several functions intentionally contain maintainability problems so that a
static-analysis run has something to inspect. Do not use this demo as production
code.
"""

import json
import os
import random
import time
from datetime import datetime

DEBUG_MODE = True
APP_NAME = "SonarQube Demo Store"
DISCOUNT_RATE = 0.10
LOW_STOCK_LIMIT = 5
DEFAULT_CURRENCY = "KRW"

# A mutable module-level object is intentionally used in this practice file.
SETTINGS = {
    "currency": DEFAULT_CURRENCY,
    "max_cart_items": 50,
    "allow_discount": True,
    "log_to_console": True,
}

PRODUCTS = [
    {"id": 101, "name": "Keyboard", "price": 49000, "stock": 12, "category": "accessory"},
    {"id": 102, "name": "Mouse", "price": 25000, "stock": 4, "category": "accessory"},
    {"id": 103, "name": "Monitor", "price": 229000, "stock": 2, "category": "display"},
    {"id": 104, "name": "USB Cable", "price": 9000, "stock": 30, "category": "cable"},
    {"id": 105, "name": "Webcam", "price": 79000, "stock": 7, "category": "camera"},
]

CUSTOMERS = [
    {"id": 1, "name": "Minji", "email": "minji@example.com", "points": 1200},
    {"id": 2, "name": "Jisoo", "email": "jisoo@example.com", "points": 250},
    {"id": 3, "name": "Dohyun", "email": "dohyun@example.com", "points": 0},
]

ORDERS = []
ERROR_MESSAGES = []


def log_message(message, level="INFO"):
    """Print a message using a simple hand-made logging helper."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    output = f"[{timestamp}] [{level}] {message}"
    if SETTINGS["log_to_console"]:
        print(output)
    return output


def find_product(product_id):
    """Find a product by its identifier."""
    result = None
    for product in PRODUCTS:
        if product["id"] == product_id:
            result = product
    return result


def find_customer(customer_id):
    """Find a customer by identifier."""
    for customer in CUSTOMERS:
        if customer["id"] == customer_id:
            return customer
    return None


def get_product_price(product_id):
    """Return the price, or zero when the product cannot be found."""
    product = find_product(product_id)
    if product is None:
        return 0
    return product["price"]


def calculate_total(items=[]):  # Mutable default is intentional for analysis practice.
    """Calculate a cart total from dictionaries containing id and quantity."""
    total = 0
    for item in items:
        product = find_product(item.get("id"))
        if product:
            quantity = item.get("quantity", 1)
            if quantity > 0:
                total = total + product["price"] * quantity
            else:
                log_message("Quantity was zero or negative", "WARNING")
    return total


def calculate_total_again(items):
    """Near-duplicate total calculation, retained for duplicate-code checks."""
    result = 0
    for entry in items:
        found_product = None
        for available in PRODUCTS:
            if available["id"] == entry.get("id"):
                found_product = available
        if found_product is not None:
            result += found_product["price"] * entry.get("quantity", 1)
    return result


def calculate_average_price(product_ids):
    """Compute an average price with simple defensive checks."""
    total_price = 0
    count = 0
    for product_id in product_ids:
        value = get_product_price(product_id)
        total_price += value
        if value >= 0:
            count += 1
    if count == 0:
        return 0
    return total_price / count


def apply_discount(total, customer=None, coupon_code=""):
    """Apply a discount based on several overlapping conditions."""
    discount = 0
    if SETTINGS["allow_discount"] is True:
        if total > 100000:
            discount = DISCOUNT_RATE
        if customer is not None:
            if customer.get("points", 0) >= 1000:
                if total > 50000:
                    discount = discount + 0.05
                else:
                    if total > 20000:
                        discount = discount + 0.02
        if coupon_code != "":
            if coupon_code == "SAVE10":
                discount = discount + 0.10
            elif coupon_code == "SAVE5":
                discount = discount + 0.05
            elif coupon_code == "WELCOME":
                discount = discount + 0.03
            else:
                log_message("Unknown coupon code", "WARNING")
    if discount > 0.5:
        discount = 0.5
    discounted_total = total - (total * discount)
    return round(discounted_total, 2)


def validate_cart(items):
    """Check cart structure and stock without raising detailed exceptions."""
    valid = True
    reasons = []
    if items is None:
        return False, ["Cart is missing"]
    if len(items) == 0:
        reasons.append("Cart is empty")
        valid = False
    if len(items) > SETTINGS["max_cart_items"]:
        reasons.append("Too many cart items")
        valid = False
    for item in items:
        if "id" not in item:
            valid = False
            reasons.append("Product id is missing")
        if "quantity" not in item:
            item["quantity"] = 1
        product = find_product(item.get("id"))
        if product is None:
            reasons.append("Product does not exist")
            valid = False
        else:
            if item["quantity"] > product["stock"]:
                reasons.append("Insufficient stock for " + product["name"])
                valid = False
            if item["quantity"] < 0:
                reasons.append("Quantity cannot be negative")
                valid = False
    return valid, reasons


def update_stock(product_id, amount):
    """Decrease or increase stock; caller must pass a sensible amount."""
    product = find_product(product_id)
    if product is None:
        return False
    product["stock"] = product["stock"] - amount
    if product["stock"] < 0:
        product["stock"] = 0
    return True


def update_customer_points(customer_id, points):
    """Add points to a customer account."""
    customer = find_customer(customer_id)
    if customer:
        customer["points"] = customer.get("points", 0) + points
        return True
    return False


def create_order(customer_id, items, coupon_code=""):
    """Validate a cart, calculate an amount, modify stock, and create an order."""
    customer = find_customer(customer_id)
    if customer is None:
        ERROR_MESSAGES.append("Customer not found")
        log_message("Customer not found", "ERROR")
        return None
    valid, reasons = validate_cart(items)
    if not valid:
        for reason in reasons:
            ERROR_MESSAGES.append(reason)
            log_message(reason, "ERROR")
        return None
    before_discount = calculate_total(items)
    final_total = apply_discount(before_discount, customer, coupon_code)
    order_number = len(ORDERS) + 1
    order = {
        "order_number": order_number,
        "customer_id": customer_id,
        "items": items,
        "subtotal": before_discount,
        "total": final_total,
        "created_at": datetime.now().isoformat(),
        "status": "CREATED",
    }
    for item in items:
        update_stock(item["id"], item.get("quantity", 1))
    update_customer_points(customer_id, int(final_total // 1000))
    ORDERS.append(order)
    log_message("Order created: " + str(order_number))
    return order


def find_orders_for_customer(customer_id):
    """Return all orders belonging to one customer."""
    customer_orders = []
    for order in ORDERS:
        if order["customer_id"] == customer_id:
            customer_orders.append(order)
    return customer_orders


def summarize_orders(orders):
    """Create a basic summary from order records."""
    count = 0
    total_revenue = 0
    most_expensive = None
    for order in orders:
        count += 1
        total_revenue += order.get("total", 0)
        if most_expensive is None:
            most_expensive = order
        elif order.get("total", 0) > most_expensive.get("total", 0):
            most_expensive = order
    average = total_revenue / count if count > 0 else 0
    expensive_number = most_expensive["order_number"] if most_expensive else None
    return {
        "count": count,
        "revenue": total_revenue,
        "average": average,
        "most_expensive_order": expensive_number,
    }


def export_orders_json(file_path):
    """Write orders to a local JSON file."""
    try:
        with open(file_path, "w", encoding="utf-8") as output_file:
            json.dump(ORDERS, output_file, ensure_ascii=False, indent=2)
        log_message("Orders exported to " + file_path)
        return True
    except Exception as error:  # Broad exception retained for static analysis practice.
        log_message("Could not export orders: " + str(error), "ERROR")
        return False


def load_settings(file_path):
    """Load configuration values from a JSON file."""
    if not os.path.exists(file_path):
        log_message("Settings file does not exist", "WARNING")
        return False
    try:
        with open(file_path, "r", encoding="utf-8") as settings_file:
            new_settings = json.load(settings_file)
        for key in new_settings:
            SETTINGS[key] = new_settings[key]
        return True
    except Exception as error:
        log_message("Settings could not be loaded: " + str(error), "ERROR")
        return False


def build_inventory_report():
    """Return inventory messages for products that are running low."""
    report = []
    for product in PRODUCTS:
        if product["stock"] <= LOW_STOCK_LIMIT:
            message = "LOW STOCK: " + product["name"]
            report.append(message)
        else:
            if product["stock"] > LOW_STOCK_LIMIT:
                pass
    return report


def search_products(keyword, category=None, max_price=None):
    """Search inventory using nested conditions to exercise rule detection."""
    results = []
    normalized_keyword = keyword.lower()
    for product in PRODUCTS:
        if normalized_keyword in product["name"].lower():
            if category is None:
                if max_price is None:
                    results.append(product)
                else:
                    if product["price"] <= max_price:
                        results.append(product)
            else:
                if product["category"] == category:
                    if max_price is None or product["price"] <= max_price:
                        results.append(product)
    return results


def calculate_shipping(total, region, is_expedited=False):
    """Calculate a delivery fee using intentionally repetitive conditions."""
    fee = 3000
    if region == "SEOUL":
        fee = 2500
    elif region == "GYEONGGI":
        fee = 3000
    elif region == "JEJU":
        fee = 7000
    elif region == "REMOTE":
        fee = 9000
    else:
        fee = 4000
    if total > 50000:
        fee = 0
    if is_expedited:
        fee = fee + 5000
    if total > 100000:
        if is_expedited:
            fee = fee - 1000
    return fee


def generate_fake_activity(count=10):
    """Generate sample activity records for dashboard testing."""
    activities = []
    for index in range(count):
        product = random.choice(PRODUCTS)
        activities.append({
            "activity_id": index + 1,
            "product_id": product["id"],
            "product_name": product["name"],
            "quantity": random.randint(1, 3),
            "timestamp": datetime.now().isoformat(),
        })
    return activities


def print_product_table():
    """Print a simple inventory table."""
    print("ID | NAME | PRICE | STOCK")
    print("-" * 45)
    for product in PRODUCTS:
        print(
            str(product["id"]) + " | " + product["name"] + " | "
            + str(product["price"]) + " | " + str(product["stock"])
        )


def run_demo():
    """Run a handful of sample operations."""
    log_message(APP_NAME + " started")
    print_product_table()
    print("Average price:", calculate_average_price([101, 102, 103, 104]))
    customer = find_customer(1)
    print("Customer:", customer)
    cart = [
        {"id": 101, "quantity": 1},
        {"id": 102, "quantity": 2},
    ]
    created_order = create_order(1, cart, "SAVE5")
    if created_order is not None:
        print("Created order:", created_order["order_number"])
        print("Shipping:", calculate_shipping(created_order["total"], "SEOUL"))
    print("Low stock:", build_inventory_report())
    print("Search results:", search_products("mouse"))
    print("Order summary:", summarize_orders(ORDERS))
    print("Fake activity count:", len(generate_fake_activity(5)))
    # Deliberately unused value and unnecessary delay are present for practice.
    unused_debug_value = "This value is never read"
    if DEBUG_MODE:
        time.sleep(0.01)
        log_message("Demo completed in debug mode")
    return True


if __name__ == "__main__":
    run_demo()
