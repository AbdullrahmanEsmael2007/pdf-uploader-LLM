import wikipedia
from fpdf import FPDF
import unicodedata

AMOUNT = 5

for i in range(AMOUNT):
    title = wikipedia.random()
    page = wikipedia.page(title)
    text = page.content
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')
    
    PDFTITLE = title.replace(" ", "_")
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt=text)
    pdf.output(f"wikipedia_pdfs/{PDFTITLE}.pdf")