from docxtpl import DocxTemplate
from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

def create_template():
    # Create a new Document
    doc = Document()
    
    # Set up styles
    styles = doc.styles
    
    # Title style
    title_style = styles['Title']
    title_font = title_style.font
    title_font.name = 'Calibri'
    title_font.size = Pt(24)
    title_font.bold = True
    
    # Heading 1 style
    heading1_style = styles['Heading 1']
    heading1_font = heading1_style.font
    heading1_font.name = 'Calibri'
    heading1_font.size = Pt(16)
    heading1_font.bold = True
    
    # Normal style
    normal_style = styles['Normal']
    normal_font = normal_style.font
    normal_font.name = 'Calibri'
    normal_font.size = Pt(11)
    
    # Add title
    title = doc.add_heading('Konsultprofil', level=0)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    # Add template variables
    doc.add_paragraph('{{name}}')
    doc.add_paragraph('{{slogan}}')
    doc.add_paragraph()
    
    # Summary section
    doc.add_heading('Sammanfattning', level=1)
    doc.add_paragraph('{{summary}}')
    doc.add_paragraph()
    
    # Expertise section
    doc.add_heading('Expertis', level=1)
    doc.add_paragraph('{% for skill in expertise %}{{skill}}{% if not loop.last %}, {% endif %}{% endfor %}')
    doc.add_paragraph()
    
    # Assignments section
    doc.add_heading('Uppdrag', level=1)
    doc.add_paragraph('{% for assignment in assignment %}')
    doc.add_paragraph('Roll: {{assignment.role}}')
    doc.add_paragraph('Kund: {{assignment.client}}')
    doc.add_paragraph('Period: {{assignment.period}}')
    doc.add_paragraph('Beskrivning: {{assignment.description}}')
    doc.add_paragraph('Approach: {{assignment.approach}}')
    doc.add_paragraph('{% endfor %}')
    
    # Contact information
    doc.add_heading('Kontaktinformation', level=1)
    doc.add_paragraph('Email: {{email}}')
    doc.add_paragraph('Telefon: {{phone}}')
    doc.add_paragraph('LinkedIn: {{linkedin}}')
    doc.add_paragraph('Plats: {{location}}')
    doc.add_paragraph()
    
    # Technical skills
    doc.add_heading('Teknisk kompetens', level=1)
    doc.add_paragraph('Teknologier: {% for tech in technologies %}{{tech}}{% if not loop.last %}, {% endif %}{% endfor %}')
    doc.add_paragraph('Metoder: {% for method in methods %}{{method}}{% if not loop.last %}, {% endif %}{% endfor %}')
    doc.add_paragraph('Verktyg: {% for tool in tools %}{{tool}}{% if not loop.last %}, {% endif %}{% endfor %}')
    doc.add_paragraph()
    
    # Languages
    doc.add_heading('Språk', level=1)
    doc.add_paragraph('{% for lang in languages %}{{lang.language}}: {{lang.level}}{% if not loop.last %}\n{% endif %}{% endfor %}')
    doc.add_paragraph()
    
    # Education
    doc.add_heading('Utbildning', level=1)
    doc.add_paragraph('{% for edu in education %}')
    doc.add_paragraph('Institution: {{edu.institution}}')
    doc.add_paragraph('Fokus: {{edu.focus}}')
    doc.add_paragraph('Period: {{edu.period}}')
    doc.add_paragraph('{% endfor %}')
    
    # Certifications
    doc.add_heading('Certifieringar', level=1)
    doc.add_paragraph('{% for cert in certifications %}{{cert}}{% if not loop.last %}, {% endif %}{% endfor %}')
    doc.add_paragraph()
    
    # Employment information
    doc.add_heading('Anställningsinformation', level=1)
    doc.add_paragraph('Anställningstyp: {{employment_type}}')
    doc.add_paragraph('Anställd av: {{employment_by}}')
    
    # Save the template
    doc.save('konsultprofil_template.docx')

if __name__ == '__main__':
    create_template() 