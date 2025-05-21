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
        raise Exception(f"Fel vid läsning av JSON-filen: {str(e)}")
    except Exception as e:
        raise Exception(f"Ett fel uppstod: {str(e)}")

def generate_output_filename(json_file_path):
    """
    Generates an output filename based on the input JSON filename and current timestamp.
    """
    # Get the base name without extension
    base_name = os.path.splitext(os.path.basename(json_file_path))[0]
    # Get current timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{base_name}_{timestamp}.docx"

def process_template(json_file_path, output_dir):
    """
    Process a Word template using JSON data and save to specified output directory.
    
    Args:
        json_file_path (str): Path to the JSON file containing template data
        output_dir (str): Directory where the processed document should be saved
    
    Returns:
        str: Path to the generated document
    """
    # Path to your template
    template_path = "Mall 0.2.docx"
    
    # Load JSON data
    context = load_json_data(json_file_path)
    
    # Generate output filename and path
    output_filename = generate_output_filename(json_file_path)
    output_path = os.path.join(output_dir, output_filename)
    
    try:
        # Load the template
        doc = DocxTemplate(template_path)
        
        # Render the template with the provided context
        doc.render(context)
        
        # Save the rendered document
        doc.save(output_path)
        return output_path
        
    except Exception as e:
        raise Exception(f"Fel vid bearbetning av mall: {str(e)}")

def main():
    # Let user select JSON file
    print("Välj en JSON-fil med data för mallen...")
    json_file_path = select_json_file()
    
    if not json_file_path:
        print("Ingen fil valdes. Avslutar programmet.")
        return
    
    # Let user choose output directory
    root = tk.Tk()
    root.withdraw()
    output_dir = filedialog.askdirectory(
        title="Välj utmapp för den genererade filen"
    )
    
    if not output_dir:
        print("Ingen utmapp valdes. Avslutar programmet.")
        return
    
    try:
        output_path = process_template(json_file_path, output_dir)
        print(f"Dokument har genererats: {output_path}")
    except Exception as e:
        print(f"Ett fel uppstod: {str(e)}")

if __name__ == "__main__":
    main() 