import random
import wikipedia
from fpdf import FPDF
import os
import unicodedata

def fetch_random_wikipedia_text():
    """Fetch a random Wikipedia article's summary."""
    try:
        random_title = wikipedia.random()
        summary = wikipedia.summary(random_title, sentences=random.randint(5, 15))
        return f"Title: {random_title}\n\n{summary}"
    except Exception as e:
        return f"Error fetching Wikipedia article: {e}"

def remove_non_ascii(text):
    """Remove non-ASCII characters from text."""
    return unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')

def generate_pdf_with_wikipedia_content(filename='random_pdf.pdf', num_pages=5):
    """Generate a PDF with random Wikipedia articles."""
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    for _ in range(num_pages):
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        article_text = fetch_random_wikipedia_text()
        safe_text = remove_non_ascii(article_text)  # Remove non-ASCII characters
        pdf.multi_cell(0, 10, safe_text)

    pdf.output(filename)
    print(f"PDF saved as {filename}")

def generate_multiple_pdfs_with_wikipedia(output_dir='wikipedia_pdfs', count=5):
    """Generate multiple random PDF files with Wikipedia content."""
    os.makedirs(output_dir, exist_ok=True)
    for i in range(count):
        filename = os.path.join(output_dir, f"wikipedia_pdf_{i+1}.pdf")
        generate_pdf_with_wikipedia_content(filename, num_pages=random.randint(1, 5))

if __name__ == "__main__":
    generate_multiple_pdfs_with_wikipedia(count=5)  # Change count as needed
