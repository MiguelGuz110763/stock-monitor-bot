import yfinance as yf
from report_generator import generate_report
from email_sender import send_email
from whatsapp_sender import send_whatsapp
import yaml

with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

stocks = config["stocks"]
email_to = config["email_to"]
whatsapp_to = config["whatsapp_to"]

def run_bot():
    data = {}
    for symbol in stocks:
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period="1d")
        price = hist["Close"][0]
        data[symbol] = price

    report = generate_report(data)
    send_email(report, email_to)
    send_whatsapp(report, whatsapp_to)

if __name__ == "__main__":
    run_bot()
