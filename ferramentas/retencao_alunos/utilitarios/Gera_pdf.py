from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph

class Gera_pdf():

    def __init__(self, data, titulo):
        self.data = data
        self.titulo = titulo

    def gera_pdf(self):


        table_data = [["Disciplina", "Número de Atrasados"]]
        data = []

        for disciplina, atrasados in self.data.items():
            row = [disciplina, atrasados]
            table_data.append(row)
            data.append(row)

        doc = SimpleDocTemplate("relatorio.pdf", pagesize=letter)
        styles = getSampleStyleSheet()

        title_style = styles["Title"]
        title_text = Paragraph(self.titulo, title_style)

        table = Table(table_data)
        table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                                ]))
        
        
        content = [title_text, table]
        doc.build(content)

 