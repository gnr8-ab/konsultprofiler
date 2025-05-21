from docx import Document
import re
from collections import defaultdict

def analyze_template_tags(doc_path):
    # Load the document
    doc = Document(doc_path)
    
    # Regular expressions for different types of Jinja2 tags
    variable_pattern = r'{{(.*?)}}'
    control_pattern = r'{%(.*?)%}'
    
    # Store findings
    variables = set()
    control_structures = defaultdict(int)
    loops = set()
    
    # Analyze each paragraph
    for para in doc.paragraphs:
        text = para.text
        
        # Find variables
        var_matches = re.finditer(variable_pattern, text)
        for match in var_matches:
            variables.add(match.group(1).strip())
        
        # Find control structures
        control_matches = re.finditer(control_pattern, text)
        for match in control_matches:
            control_text = match.group(1).strip()
            control_structures[control_text] += 1
            
            # Check if it's a loop
            if 'for' in control_text:
                loops.add(control_text)
    
    # Print results
    print("\n=== Template Analysis Results ===\n")
    
    print("Variables found:")
    for var in sorted(variables):
        print(f"- {var}")
    
    print("\nControl structures found:")
    for control, count in sorted(control_structures.items()):
        print(f"- {control} (used {count} times)")
    
    print("\nLoops found:")
    for loop in sorted(loops):
        print(f"- {loop}")

if __name__ == '__main__':
    analyze_template_tags('Mall 0.2.docx') 