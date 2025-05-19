from docxtpl import DocxTemplate
import os
import json
from datetime import datetime
import tkinter as tk
from tkinter import filedialog

def select_json_file():
    """
    Opens a file dialog for selecting a JSON file.
    Returns the selected file path or None if cancelled.
    """
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    file_path = filedialog.askopenfilename(
        title="Välj JSON-fil",
        filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
    )
    return file_path if file_path else None

def load_json_data(file_path):
    """
    Loads and validates JSON data from the selected file.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data
    except json.JSONDecodeError as e:
        print(f"Fel vid läsning av JSON-filen: {str(e)}")
        return None
    except Exception as e:
        print(f"Ett fel uppstod: {str(e)}")
        return None

def generate_output_filename(json_file_path):
    """
    Generates an output filename based on the input JSON filename and current timestamp.
    """
    # Get the base name without extension
    base_name = os.path.splitext(os.path.basename(json_file_path))[0]
    # Get current timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{base_name}_{timestamp}.docx"

def process_template(template_path, output_path, context):
    """
    Process a Word template using Jinja templating.
    
    Args:
        template_path (str): Path to the .docx template file
        output_path (str): Path where the processed document should be saved
        context (dict): Dictionary containing the variables to be used in the template
    """
    try:
        # Load the template
        doc = DocxTemplate(template_path)
        
        # Render the template with the provided context
        doc.render(context)
        
        # Save the rendered document
        doc.save(output_path)
        print(f"Dokument har genererats: {output_path}")
        
    except Exception as e:
        print(f"Fel vid bearbetning av mall: {str(e)}")

def main():
    # Path to your template
    template_path = "Mall 0.2.docx"
    
    # Let user select JSON file
    print("Välj en JSON-fil med data för mallen...")
    json_file_path = select_json_file()
    
    if not json_file_path:
        print("Ingen fil valdes. Avslutar programmet.")
        return
    
    # Load JSON data
    context = load_json_data(json_file_path)
    if not context:
        print("Kunde inte läsa in JSON-data. Avslutar programmet.")
        return
    
    # Generate output filename
    base_name = os.path.splitext(os.path.basename(json_file_path))[0]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    default_filename = f"{base_name}_{timestamp}.docx"
    
    # Let user choose where to save the file
    root = tk.Tk()
    root.withdraw()
    output_path = filedialog.asksaveasfilename(
        title="Välj var du vill spara den genererade filen",
        defaultextension=".docx",
        initialfile=default_filename,
        filetypes=[("Word documents", "*.docx"), ("All files", "*.*")]
    )
    
    if not output_path:
        print("Ingen sparplats valdes. Avslutar programmet.")
        return
    
    # Process the template
    process_template(template_path, output_path, context)

if __name__ == "__main__":
    main() 