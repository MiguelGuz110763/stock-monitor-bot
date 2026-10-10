def generate_report(data):
    report = "📊 *Reporte de Acciones del Día*\n\n"
    for symbol, price in data.items():
        report += f"• {symbol}: ${price:.2f}\n"
    report += "\nGenerado automáticamente por el bot."
    return report
