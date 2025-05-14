from docxtpl import DocxTemplate
import json

def generate_profile(json_file):
    # Load the JSON data
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Load the template
    doc = DocxTemplate('konsultprofil_template.docx')
    
    # Render the template with the JSON data
    doc.render(data)
    
    # Save the generated profile
    output_file = f"{data['name'].lower().replace(' ', '_')}_profil.docx"
    doc.save(output_file)
    print(f"Profile generated: {output_file}")

if __name__ == '__main__':
    generate_profile('consultant_profile.json') 