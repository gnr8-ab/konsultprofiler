import streamlit as st
import json
import os
from docxtpl import DocxTemplate
from datetime import datetime

def generate_output_filename(json_file_path):
    """
    Generates an output filename based on the input JSON filename and current timestamp.
    """
    # Get the base name without extension
    base_name = os.path.splitext(os.path.basename(json_file_path))[0]
    # Get current timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{base_name}_{timestamp}.docx"

def process_template(data, output_filename):
    """
    Process a Word template using JSON data and return the document bytes.
    """
    # Path to your template
    template_path = "Mall 0.2.docx"
    
    try:
        # Load the template
        doc = DocxTemplate(template_path)
        
        # Render the template with the provided context
        doc.render(data)
        
        # Save to a temporary file and read bytes
        temp_path = f"temp_{output_filename}"
        doc.save(temp_path)
        
        with open(temp_path, 'rb') as file:
            doc_bytes = file.read()
        
        # Clean up temporary file
        os.remove(temp_path)
        
        return doc_bytes
        
    except Exception as e:
        st.error(f"Fel vid bearbetning av mall: {str(e)}")
        return None

st.title("Konsultprofil Generator")

# File uploader for input file
uploaded_file = st.file_uploader("Välj en JSON-fil att redigera", type=['json'])

if uploaded_file is not None:
    # Read the uploaded file
    content = uploaded_file.getvalue().decode("utf-8")
    try:
        data = json.loads(content)
        
        # Display and edit the data
        st.subheader("Grundläggande information")
        
        # Basic information
        data['name'] = st.text_input("Namn", value=data.get('name', ''))
        data['slogan'] = st.text_input("Slogan", value=data.get('slogan', ''))
        data['summary'] = st.text_area("Sammanfattning", value=data.get('summary', ''), height=150)
        
        # Expertise
        st.subheader("Expertis")
        expertise = data.get('expertise', [])
        for i in range(3):
            if i < len(expertise):
                expertise[i] = st.text_input(f"Expertis {i+1}", value=expertise[i])
            else:
                expertise.append(st.text_input(f"Expertis {i+1}", value=""))
        data['expertise'] = expertise

        # Assignments
        st.subheader("Uppdrag")
        assignments = data.get('assignment', [])
        
        # Add new assignment button
        if st.button("Lägg till nytt uppdrag"):
            assignments.append({
                "role": "",
                "client": "",
                "period": "",
                "description": "",
                "approach": ""
            })
        
        # Display existing assignments
        for i, assignment in enumerate(assignments):
            st.markdown(f"### Uppdrag {i+1}")
            col1, col2 = st.columns(2)
            with col1:
                assignment['role'] = st.text_input(f"Roll {i+1}", value=assignment.get('role', ''))
                assignment['client'] = st.text_input(f"Kund {i+1}", value=assignment.get('client', ''))
            with col2:
                assignment['period'] = st.text_input(f"Period {i+1}", value=assignment.get('period', ''))
            
            assignment['description'] = st.text_area(f"Beskrivning {i+1}", value=assignment.get('description', ''), height=100)
            assignment['approach'] = st.text_area(f"Approach {i+1}", value=assignment.get('approach', ''), height=100)
            
            if st.button(f"Ta bort uppdrag {i+1}", key=f"remove_{i}"):
                assignments.pop(i)
                st.rerun()
        
        data['assignment'] = assignments

        # Contact Information
        st.subheader("Kontaktinformation")
        col1, col2 = st.columns(2)
        with col1:
            data['email'] = st.text_input("E-post", value=data.get('email', ''))
            data['phone'] = st.text_input("Telefon", value=data.get('phone', ''))
        with col2:
            data['linkedin'] = st.text_input("LinkedIn", value=data.get('linkedin', ''))
            data['location'] = st.text_input("Plats", value=data.get('location', ''))

        # Skills and Technologies
        st.subheader("Kompetenser och verktyg")
        col1, col2, col3 = st.columns(3)
        with col1:
            technologies = data.get('technologies', [])
            st.write("Teknologier")
            for i in range(3):
                if i < len(technologies):
                    technologies[i] = st.text_input(f"Teknologi {i+1}", value=technologies[i], key=f"tech_{i}")
                else:
                    technologies.append(st.text_input(f"Teknologi {i+1}", value="", key=f"tech_{i}"))
            data['technologies'] = technologies

        with col2:
            methods = data.get('methods', [])
            st.write("Metoder")
            for i in range(3):
                if i < len(methods):
                    methods[i] = st.text_input(f"Metod {i+1}", value=methods[i], key=f"method_{i}")
                else:
                    methods.append(st.text_input(f"Metod {i+1}", value="", key=f"method_{i}"))
            data['methods'] = methods

        with col3:
            tools = data.get('tools', [])
            st.write("Verktyg")
            for i in range(3):
                if i < len(tools):
                    tools[i] = st.text_input(f"Verktyg {i+1}", value=tools[i], key=f"tool_{i}")
                else:
                    tools.append(st.text_input(f"Verktyg {i+1}", value="", key=f"tool_{i}"))
            data['tools'] = tools

        # Languages
        st.subheader("Språk")
        languages = data.get('languages', [
            {"language": "Swedish", "level": ""},
            {"language": "English", "level": ""},
            {"language": "Spanish", "level": ""}
        ])
        
        for i, lang in enumerate(languages):
            col1, col2 = st.columns(2)
            with col1:
                lang['language'] = st.text_input(f"Språk {i+1}", value=lang.get('language', ''), key=f"lang_{i}")
            with col2:
                lang['level'] = st.text_input(f"Nivå {i+1}", value=lang.get('level', ''), key=f"level_{i}")
        data['languages'] = languages

        # Education
        st.subheader("Utbildning")
        education = data.get('education', [])
        
        if st.button("Lägg till utbildning"):
            education.append({
                "institution": "",
                "focus": "",
                "period": ""
            })
        
        for i, edu in enumerate(education):
            st.markdown(f"### Utbildning {i+1}")
            col1, col2 = st.columns(2)
            with col1:
                edu['institution'] = st.text_input(f"Institution {i+1}", value=edu.get('institution', ''), key=f"inst_{i}")
                edu['focus'] = st.text_input(f"Inriktning {i+1}", value=edu.get('focus', ''), key=f"focus_{i}")
            with col2:
                edu['period'] = st.text_input(f"Period {i+1}", value=edu.get('period', ''), key=f"edu_period_{i}")
            
            if st.button(f"Ta bort utbildning {i+1}", key=f"remove_edu_{i}"):
                education.pop(i)
                st.rerun()
        
        data['education'] = education

        # Certifications
        st.subheader("Certifieringar")
        certifications = data.get('certifications', [])
        for i in range(2):
            if i < len(certifications):
                certifications[i] = st.text_input(f"Certifiering {i+1}", value=certifications[i], key=f"cert_{i}")
            else:
                certifications.append(st.text_input(f"Certifiering {i+1}", value="", key=f"cert_{i}"))
        data['certifications'] = certifications

        # Employment Information
        st.subheader("Anställningsinformation")
        col1, col2 = st.columns(2)
        with col1:
            data['employment_type'] = st.text_input("Anställningstyp", value=data.get('employment_type', 'Consultant'))
        with col2:
            data['employment_by'] = st.text_input("Anställs av", value=data.get('employment_by', 'GNR8'))
        
        # Action buttons in columns
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Spara JSON"):
                # Create a download button for the modified JSON
                st.download_button(
                    label="Ladda ner uppdaterad JSON",
                    data=json.dumps(data, indent=2, ensure_ascii=False),
                    file_name="updated_profile.json",
                    mime="application/json"
                )
        
        with col2:
            if st.button("Generera Word-dokument"):
                output_filename = generate_output_filename(uploaded_file.name)
                doc_bytes = process_template(data, output_filename)
                
                if doc_bytes:
                    st.download_button(
                        label="Ladda ner Word-dokument",
                        data=doc_bytes,
                        file_name=output_filename,
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    )
            
    except json.JSONDecodeError:
        st.error("Felaktigt JSON-format. Vänligen ladda upp en giltig JSON-fil.")
else:
    st.info("Vänligen ladda upp en JSON-fil för att börja redigera profilen.") 