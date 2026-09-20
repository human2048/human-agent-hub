import os
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from fpdf import FPDF

def create_docx_report(title: str, content_paragraphs: list, output_path: str = "reporte.docx") -> str:
    """
    Genera un archivo .docx profesional con estilo corporativo.
    """
    doc = Document()
    
    # Configurar título principal
    heading = doc.add_heading(title, level=0)
    heading.style.font.color.rgb = RGBColor(0, 51, 102)  # Azul corporativo
    
    # Agregar párrafos
    for para in content_paragraphs:
        p = doc.add_paragraph(para)
        p.style.font.name = 'Calibri'
        p.style.font.size = Pt(11)
        
    doc.save(output_path)
    return output_path


class PDFReport(FPDF):
    def header(self):
        self.set_font('Helvetica', 'B', 12)
        self.set_text_color(0, 51, 102)
        self.cell(0, 10, 'CyberNiche Lab - Reporte Autónomo', border=False, ln=True, align='R')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f'Página {self.page_no()}', align='C')

def create_pdf_report(title: str, content_paragraphs: list, output_path: str = "reporte.pdf") -> str:
    """
    Genera un archivo .pdf limpio usando fpdf2.
    """
    pdf = PDFReport()
    pdf.add_page()
    pdf.set_font("Helvetica", size=16, style='B')
    pdf.cell(0, 10, title, ln=True, align='L')
    pdf.ln(5)
    
    pdf.set_font("Helvetica", size=11)
    for para in content_paragraphs:
        # fpdf2 soporta encode automático UTF-8 mediante multi_cell
        pdf.multi_cell(0, 8, para)
        pdf.ln(2)
        
    pdf.output(output_path)
    return output_path