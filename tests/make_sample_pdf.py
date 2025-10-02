from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

output_path = os.path.join(
    os.path.dirname(__file__), 
    "../data/raw/sample.pdf"
)

def create_sample_pdf(path):
    c = canvas.Canvas(path, pagesize=letter)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, 750, "Invoice Report")

    c.setFont("Helvetica", 12)
    c.drawString(100, 720, "Customer: John Doe")
    c.drawString(100, 700, "Date: 2025-10-02")

    # Table header
    c.drawString(100, 670, "Item")
    c.drawString(250, 670, "Qty")
    c.drawString(350, 670, "Price")

    # Table rows
    c.drawString(100, 650, "Laptop")
    c.drawString(250, 650, "1")
    c.drawString(350, 650, "$1200")

    c.drawString(100, 630, "Mouse")
    c.drawString(250, 630, "2")
    c.drawString(350, 630, "$40")

    c.save()
    print(f"✅ Sample PDF created at: {path}")

if __name__ == "__main__":
    create_sample_pdf(output_path)
