# save_pdf.py
from fpdf import FPDF




def save_text_pdf(text: str, filename: str = "rca_report.pdf", title: str = "RCA Report"):
pdf = FPDF()
pdf.set_auto_page_break(auto=True, margin=15)
pdf.add_page()


pdf.set_font("Arial", 'B', 16)
pdf.cell(0, 10, title, ln=True)
pdf.ln(6)


pdf.set_font("Arial", size=11)
for line in text.split("\n"):
pdf.multi_cell(0, 6, line)


pdf.output(filename)
return filename




if __name__ == "__main__":
sample = "Sample RCA\n- Issue: test\n- Fix: none"
print(save_text_pdf(sample, "test_rca.pdf"))
