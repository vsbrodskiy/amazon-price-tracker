# amazon-price-tracker
# Automated Amazon Price Tracker

## 📖 Description
This Python script automatically tracks the prices of multiple products on Amazon. It reads a list of product URLs from a CSV file, scrapes the current price and title for each, and logs the data to create a price history. If a product's price drops below a user-defined target, the script sends an automated email alert.

## ✨ Features
* Tracks multiple products simultaneously from Amazon.
* Scrapes real-time price and title data.
* Logs price history with timestamps to a CSV file for tracking.
* Sends an automated email alert when a product's price drops below a target.
* Securely manages email credentials using environment variables.

## 🛠️ Technologies Used
* **Python**
* **BeautifulSoup4** (for web scraping)
* **Requests** (for making HTTP requests)
* **smtplib** (for sending emails)
* **Dotenv** (for managing environment variables)

## 🚀 How to Use
1.  Clone this repository.
2.  Create a `.env` file and add your email credentials (see `.env.example` for the format).
3.  Modify `products.csv` with the Amazon URLs and target prices you want to track.
4.  Run the `main.py` script.

## 🎬 Project Demo
![Thebestpricesnotificationmain py2025-10-0317-09-28-ezgif com-resize](https://github.com/user-attachments/assets/dfbb1056-b1cd-4ab8-8024-d66d7144e488)

## Example Email Alert
<img width="1313" height="367" alt="Screenshot 2025-10-03 171943" src="https://github.com/user-attachments/assets/9dff42de-93e9-4971-acd3-dccacc615b27" />
