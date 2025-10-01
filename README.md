# amazon-price-tracker
# Automated Amazon Price Tracker

## 📖 Description
This Python script automatically tracks the prices of multiple products on Amazon. It reads a list of product URLs from a CSV file, scrapes the current price and title for each, and logs the data to create a price history. If a product's price drops below a user-defined target, the script sends an automated email alert.

## ✨ Features
* Tracks multiple products simultaneously.
* Scrapes real-time price and title data from Amazon.
* Logs price history with timestamps to a CSV file.
* Sends an email alert when a price drops below a target.
* Securely manages credentials using environment variables.

## 🛠️ Technologies Used
* **Python**
* **BeautifulSoup4** (for web scraping)
* **Requests** (for making HTTP requests)
* **smtplib** (for sending emails)
* **Dotenv** (for managing environment variables)

## 🚀 How to Use
1.  Clone this repository.
2.  Create a `.env` file and add your email credentials (see `.env.example`).
3.  Update the `products.csv` file with the Amazon URLs and target prices you want to track.
4.  Run the `main.py` script.
