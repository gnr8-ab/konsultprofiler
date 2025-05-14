from docxtpl import DocxTemplate
from docx2pdf import convert
import json
import os
import sys

def generate_profile(json_file):
    try:
        # Load the JSON data
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print("✓ JSON data loaded successfully")
        
        # Load the template
        doc = DocxTemplate('konsultprofil_template.docx')
        print("✓ Template loaded successfully")
        
        # Render the template with the JSON data
        doc.render(data)
        print("✓ Template rendered with data")
        
        # Generate base filename
        base_filename = data['name'].lower().replace(' ', '_')
        
        # Save the generated profile as DOCX
        docx_file = f"{base_filename}_profil.docx"
        
        # Check if file is already open
        if os.path.exists(docx_file):
            try:
                with open(docx_file, 'a'):
                    pass
            except PermissionError:
                print(f"Error: {docx_file} is currently open. Please close it and try again.")
                return
        
        doc.save(docx_file)
        print(f"✓ DOCX profile generated: {docx_file}")
        
        # Convert to PDF
        pdf_file = f"{base_filename}_profil.pdf"
        print(f"Converting to PDF: {pdf_file}")
        convert(docx_file, pdf_file)
        print(f"✓ PDF profile generated: {pdf_file}")
        
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        print(f"Error type: {type(e).__name__}")
        import traceback
        print("Full error traceback:")
        traceback.print_exc()

if __name__ == '__main__':
    print("Starting profile generation...")
    generate_profile('consultant_profile.json') 