import tkinter as tk
from tkinter import filedialog, messagebox
import os
from template_processor import process_template

class KonsultprofilerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Konsultprofiler")
        self.root.geometry("600x400")
        
        # Skapa huvudram
        main_frame = tk.Frame(root, padx=20, pady=20)
        main_frame.pack(expand=True, fill='both')
        
        # Titel
        title_label = tk.Label(main_frame, text="Konsultprofiler", font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # JSON-fil väljare
        json_frame = tk.Frame(main_frame)
        json_frame.pack(fill='x', pady=10)
        
        json_label = tk.Label(json_frame, text="Välj JSON-fil:", width=15)
        json_label.pack(side='left')
        
        self.json_path = tk.StringVar()
        json_entry = tk.Entry(json_frame, textvariable=self.json_path, width=50)
        json_entry.pack(side='left', padx=5)
        
        json_button = tk.Button(json_frame, text="Bläddra", command=self.select_json)
        json_button.pack(side='left')
        
        # Utmapp väljare
        output_frame = tk.Frame(main_frame)
        output_frame.pack(fill='x', pady=10)
        
        output_label = tk.Label(output_frame, text="Välj utmapp:", width=15)
        output_label.pack(side='left')
        
        self.output_path = tk.StringVar()
        output_entry = tk.Entry(output_frame, textvariable=self.output_path, width=50)
        output_entry.pack(side='left', padx=5)
        
        output_button = tk.Button(output_frame, text="Bläddra", command=self.select_output)
        output_button.pack(side='left')
        
        # Kör-knapp
        run_button = tk.Button(main_frame, text="Generera dokument", command=self.run_processor, 
                             bg="#4CAF50", fg="white", font=("Arial", 12), padx=20, pady=10)
        run_button.pack(pady=20)
        
        # Status
        self.status_var = tk.StringVar()
        status_label = tk.Label(main_frame, textvariable=self.status_var, fg="gray")
        status_label.pack(pady=10)
        
        # Sätt standardvärden
        self.output_path.set(os.path.expanduser("~/Downloads"))
    
    def select_json(self):
        filename = filedialog.askopenfilename(
            title="Välj JSON-fil",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if filename:
            self.json_path.set(filename)
    
    def select_output(self):
        dirname = filedialog.askdirectory(
            title="Välj utmapp"
        )
        if dirname:
            self.output_path.set(dirname)
    
    def run_processor(self):
        json_file = self.json_path.get()
        output_dir = self.output_path.get()
        
        if not json_file:
            messagebox.showerror("Fel", "Välj en JSON-fil först!")
            return
        
        if not output_dir:
            messagebox.showerror("Fel", "Välj en utmapp först!")
            return
        
        try:
            self.status_var.set("Genererar dokument...")
            self.root.update()
            
            output_file = process_template(json_file, output_dir)
            
            self.status_var.set(f"Dokument genererat: {output_file}")
            messagebox.showinfo("Klar!", f"Dokumentet har genererats:\n{output_file}")
            
        except Exception as e:
            self.status_var.set("Ett fel uppstod!")
            messagebox.showerror("Fel", str(e))

def main():
    root = tk.Tk()
    app = KonsultprofilerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 