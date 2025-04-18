from fpdf import FPDF
from app.tickets.utils import generate_barcode_memory
from datetime import datetime

class TicketSale(FPDF):
    def __init__(self, products, ticket_id, company, nit, cash, due):
        super().__init__("P", "mm", (80, 50 + (len(products) * 3 + 35)) )
        self.set_margins(5, 5, 5)
        self.set_auto_page_break(auto=True, margin=5)
        self.items = products
        self.subtotal = 0
        self.company = company
        self.ticket_id = ticket_id
        self.nit = nit
        self.cash = cash
        self.due = due

    def header(self):
        """Ticket header with logo and store data."""
        self.set_text_color(68, 64, 60)

        self.set_font("Helvetica", size=10)
        self.cell(70, 2, "- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -", ln=True, align="C")
        self.cell(70, 2, "- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -", ln=True, align="C")
        
        self.set_font("Helvetica", "B", 15)
        self.cell(70, 10, "TICKET", ln=True, align="C")

        self.set_font("Helvetica", size=10)
        self.cell(70, 0, "- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -", ln=True, align="C")
        self.cell(70, 4, "- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -", ln=True, align="C")
        
        self.ln(2)

    def footer(self):
        """Footer with thank you message."""

        self.set_y(-20)

        self.set_text_color(68, 64, 60)
        self.set_font("Helvetica", size=10)
        self.cell(70, 0, "- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -", ln=True, align="C")
        
        barcode_img = generate_barcode_memory(self.ticket_id)
        
        temp_path = "barcode_temp.png"
        barcode_img.save(temp_path, format="PNG")
        self.image(temp_path, 0, self.get_y() + 3, 80, 10)
        
    def add_items(self):
        """Add information about products for sale."""
        self.set_text_color(68, 64, 60)
        self.set_font("Courier", size=9)
        for item in self.items:
            total_item = item.quantity * item.price
            self.subtotal += total_item

            self.cell(7, 3, str(item.quantity), align="C")
            self.cell(35, 3, item.name[:20], align="L")
            self.cell(25, 3, f"${total_item:,.2f}", align="R")
            self.ln()

        self.ln(h=5)

    def add_company_info(self):
        """Add information about company."""
        self.set_text_color(68, 64, 60)
        self.set_font("Courier", size=9) 

        self.cell(0, 4, f" {self.company}", align="L")
        self.ln()
        self.cell(0, 4, f" NIT: {self.nit}", align="L")
        self.ln()
        self.cell(0, 4, f" {datetime.now()}", align="L")

    def add_info_cash(self):
        """Add information about cash for sale."""
        # Totales
        iva = self.subtotal * 0.19
        total = self.subtotal + iva
        
        self.set_font("Helvetica", size=10)
        self.cell(70, 0, "- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -", ln=True, align="C")
        
        self.set_font("Courier", size=9, style="B")
        self.cell(2, 7, "", align="C")
        self.cell(35, 7, "CANTIDAD TOTAL:", align="L")
        self.cell(30, 7, f"${self.subtotal:,.2f}", align="R")
        self.ln()

        self.set_font("Helvetica", size=10)
        self.cell(70, 0, "- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -", ln=True, align="C")

        self.set_font("Courier", size=9, style="B")
        self.cell(2, 7, "", align="C")
        self.cell(35, 4, "Efectivo:", align="L")
        self.cell(30, 4, f"${self.cash:,.2f}", align="R")
        self.ln()
        self.cell(2, 7, "", align="C")
        self.cell(35, 4, "Vueltos:", align="L")
        self.cell(30, 4, f"${self.due:,.2f}", align="R")
        self.ln()

        self.set_font("Helvetica", size=10)
        self.cell(70, 0, "- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -", ln=True, align="C")
        self.ln(h=3)

