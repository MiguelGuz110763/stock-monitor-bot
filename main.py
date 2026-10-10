import yfinance as yf
from report_generator import generate_report
from email_sender import send_email
from whatsapp_sender import send_whatsapp
import yaml

# Cargar configuración
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

stocks = config["stocks"]
email_to = config["email_to"]
whatsapp_to = config["whatsapp_to"]

def run_bot():
    report_lines = []

    for stock in stocks:
        print(f"Procesando {stock}...")

        # Descargar datos del día
        hist = yf.download(stock, period="1d")

        # Validación robusta para evitar fallos
        if hist.empty or "Close" not in hist or hist["Close"].empty:
            print(f"No hay datos disponibles para {stock}.")
            report_lines.append(f"{stock}: sin datos disponibles.")
            continue

        # Último precio disponible
        price = hist["Close"].iloc[-1]

        report_lines.append(f"{stock}: ${price:.2f}")

    # Generar reporte final
    report = generate_report(report_lines)

    # Enviar email
    send_email(report, email_to)

    # Enviar WhatsApp
    send_whatsapp(report, whatsapp_to)

# Ejecutar bot
if __name__ == "__main__":
    run_bot()
