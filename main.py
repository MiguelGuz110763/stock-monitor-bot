import yfinance as yf
from report_generator import (
    generate_report_text,
    generate_pdf,
    generate_html,
    generate_excel,
)
from email_sender import send_email
from whatsapp_sender import send_whatsapp
import yaml
import numpy as np

with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

stocks = config["stocks"]
columns = config.get("columns", ["Close"])
report_style = config.get("report_style", "excel")

export_formats = config.get("export_formats", [])

alert_threshold = config.get("alert_threshold", 3)
show_alerts = config.get("show_alerts", True)

summary_enabled = config.get("summary_enabled", True)
summary_type = config.get("summary_type", "simple")

trend_indicators = config.get("trend_indicators", True)

prediction_enabled = config.get("prediction_enabled", True)
prediction_days = config.get("prediction_days", 5)

email_to = config["email_to"]
whatsapp_to = config["whatsapp_to"]

whatsapp_send_file = config.get("whatsapp_send_file", False)
whatsapp_file_format = config.get("whatsapp_file_format", "pdf")


def get_trend_indicator(change):
    if not trend_indicators:
        return ""
    if change > 0:
        return "↑"
    elif change < 0:
        return "↓"
    else:
        return "→"


def predict_trend(stock):
    if not prediction_enabled:
        return ""

    hist = yf.download(stock, period=f"{prediction_days}d")

    if hist.empty or "Close" not in hist:
        return ""

    closes = hist["Close"].dropna()
    if len(closes) < 2:
        return ""

    slope = np.polyfit(range(len(closes)), closes, 1)[0]

    if slope > 0:
        return "Predicción: tendencia al alza."
    elif slope < 0:
        return "Predicción: tendencia a la baja."
    else:
        return "Predicción: estable."


def format_row(stock, row_data, change):
    indicator = get_trend_indicator(change)

    if report_style == "markdown":
        values = " | ".join(str(row_data[col]) for col in columns)
        return f"| {stock} {indicator} | {values} |"

    elif report_style == "emoji":
        parts = " | ".join([f"{col}: {row_data[col]}" for col in columns])
        return f"📈 {stock} {indicator} → {parts}"

    else:
        parts = "   ".join([f"{col}: {row_data[col]}" for col in columns])
        return f"{stock} {indicator}   {parts}"


def generate_summary(results):
    if not summary_enabled:
        return ""

    ups = [r for r in results if r["change"] > 0]
    downs = [r for r in results if r["change"] < 0]

    lines = []
    lines.append("RESUMEN DEL DÍA")
    lines.append("----------------")
    lines.append(f"Acciones que subieron: {len(ups)}")
    lines.append(f"Acciones que bajaron: {len(downs)}")

    if summary_type == "detailed":
        if ups:
            top_up = max(ups, key=lambda x: x["change"])
            lines.append(
                f"Mayor subida: {top_up['stock']} (+{top_up['change']:.2f}%)"
            )
        if downs:
            top_down = min(downs, key=lambda x: x["change"])
            lines.append(
                f"Mayor caída: {top_down['stock']} ({top_down['change']:.2f}%)"
            )

    lines.append("")
    return "\n".join(lines)


def run_bot():
    report_lines = []
    results = []

    if report_style == "markdown":
        header = "| Stock | " + " | ".join(columns) + " |"
        separator = "|--------|" + "|".join(["--------" for _ in columns]) + "|"
        report_lines.append(header)
        report_lines.append(separator)

    for stock in stocks:
        print(f"Procesando {stock}...")

        hist = yf.download(stock, period="2d")

        if hist.empty or "Close" not in hist:
            report_lines.append(f"{stock}: sin datos disponibles.")
            continue

        closes = hist["Close"].dropna()
        if len(closes) == 0:
            report_lines.append(f"{stock}: sin datos disponibles.")
            continue

        current_price = closes.iloc[-1]
        if len(closes) > 1:
            previous_price = closes.iloc[-2]
            change = ((current_price - previous_price) / previous_price) * 100
        else:
            change = 0

        row_data = {}
        for col in columns:
            if col not in hist or hist[col].empty:
                row_data[col] = "N/D"
            else:
                row_data[col] = round(float(hist[col].iloc[-1]), 2)

        results.append({"stock": stock, "change": change})

        report_lines.append(format_row(stock, row_data, change))

        if show_alerts and abs(change) >= alert_threshold:
            direction = "subió" if change > 0 else "bajó"
            report_lines.append(f"⚠️ ALERTA: {stock} {direction} {change:.2f}%")

        pred = predict_trend(stock)
        if pred:
            report_lines.append(pred)

        report_lines.append("")

    summary = generate_summary(results)
    final_text = generate_report_text(summary, report_lines)

    exported_files = []

    if "pdf" in export_formats:
        pdf_path = generate_pdf(final_text)
        exported_files.append(pdf_path)

    if "html" in export_formats:
        html_path = generate_html(final_text)
        exported_files.append(html_path)

    if "excel" in export_formats:
        excel_path = generate_excel(results, columns)
        exported_files.append(excel_path)

    send_email(final_text, email_to, attachments=exported_files)

    file_to_send = None
    if whatsapp_send_file:
        for f in exported_files:
            if f.endswith(whatsapp_file_format):
                file_to_send = f
                break

    send_whatsapp(final_text, whatsapp_to, file_to_send)


if __name__ == "__main__":
    run_bot()
