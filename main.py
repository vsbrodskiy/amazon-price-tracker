import requests
from bs4 import BeautifulSoup
import smtplib
import os
from dotenv import load_dotenv
import csv
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

# --- CONSTANTS ---
MY_EMAIL = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
SMTP_ADDRESS = os.getenv("SMTP_ADDRESS")
PRODUCTS_CSV = "products.csv"
PRICE_LOG_CSV = "price_log.csv"

# --- HEADERS for request to look like a real browser ---
header = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,"
              "application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 "
                  "Safari/537.36",
    "Priority": "u=0, i",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-User": "?1",
    "Sec-Fetch-Dest": "document",
}


def check_price(url, target_price):
    """Scrapes a product page, logs the price, and sends an email if the price is below target."""
    print(f"Checking price for: {url}")
    try:
        response = requests.get(url, headers=header)
        response.raise_for_status()  # Raises an exception for bad responses (4xx or 5xx)
    except requests.exceptions.RequestException as e:
        print(f"Failed to retrieve the webpage. Error: {e}")
        return

    soup = BeautifulSoup(response.content, "html.parser")

    # Find product title
    try:
        title_tag = soup.find(id="productTitle")
        product_title = title_tag.get_text().strip()
    except AttributeError:
        print(f"Could not find the product title for {url}. Amazon might be blocking the request.")
        return

    # Find product price
    try:
        price_tag = soup.find(class_="a-price aok-align-center reinventPricePriceToPayMargin priceToPay")
        price_text = price_tag.get_text()
        current_price = float(price_text.replace("$", ""))
    except (AttributeError, ValueError):
        print(f"Could not find or parse the price for {product_title}.")
        return

    # Log the price to a CSV file
    log_price(product_title, current_price)

    print(f"Found product: '{product_title}'")
    print(f"Current price: ${current_price}\n")

    # Send email alert if price is below target
    if current_price < target_price:
        send_email_alert(product_title, current_price, url)


def log_price(title, price):
    """Appends the current date, title, and price to the price_log.csv file."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    file_exists = os.path.isfile(PRICE_LOG_CSV)

    with open(PRICE_LOG_CSV, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Timestamp", "ProductTitle", "Price"])  # Write header if file is new
        writer.writerow([timestamp, title, price])


def send_email_alert(title, price, url):
    """Sends an email alert for the price drop."""
    message = f"Subject: Amazon Price Alert!\n\n{title} is now only ${price}!\n\nBuy it here:\n{url}".encode('utf-8')
    try:
        with smtplib.SMTP(SMTP_ADDRESS, port=587) as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=EMAIL_PASSWORD)
            connection.sendmail(
                from_addr=MY_EMAIL,
                to_addrs=MY_EMAIL,
                msg=message
            )
        print(f"SUCCESS: Email alert sent for {title}!")
    except smtplib.SMTPException as e:
        print(f"FAILURE: Could not send email. Error: {e}")


# --- MAIN SCRIPT EXECUTION ---
if __name__ == "__main__":
    try:
        with open(PRODUCTS_CSV, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                check_price(url=row["URL"], target_price=float(row["TargetPrice"]))
    except FileNotFoundError:
        print(f"Error: The file '{PRODUCTS_CSV}' was not found. Please create it.")