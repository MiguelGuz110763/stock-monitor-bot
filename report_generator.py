from fpdf import FPDF
import pandas as pd
import os
from datetime import datetime


def generate_report_text(summary, report_lines):
    return summary + "\n" + "\n".join(report_lines)


def generate_pdf(text, filename=None):
    if filename is None:
        filename = f"reporte_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"

    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=11)

    for line in text.split("\n"):
        pdf.multi_cell(0, 6, line)

    pdf.output(filename)
    return os.path.abspath(filename)


def generate_html(text, filename=None):
    if filename is None:
        filename = f"reporte_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"

    html_content = "<html><body><pre>" + text + "</pre></body></html>"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(html_content)

    return os.path.abspath(filename)


def generate_excel(results, columns, filename=None):
    if filename is None:
        filename = f"reporte_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"

    data = []
    for r in results:
        row = {"Stock": r["stock"], "Change_%": round(r["change"], 2)}
        data.append(row)

    df = pd.DataFrame(data)
    df.to_excel(filename, index=False)

    return os.path.abspath(filename)
