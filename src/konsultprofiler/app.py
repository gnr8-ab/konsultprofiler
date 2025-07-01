import streamlit as st
import json
import os
from docxtpl import DocxTemplate, InlineImage
from datetime import datetime
from docx.shared import Mm
from PIL import Image
import io

def generate_output_filename(json_file_path):
    """
    Generates an output filename based on the input JSON filename and current timestamp.
    """
    # Get the base name without extension
    base_name = os.path.splitext(os.path.basename(json_file_path))[0]
    # Get current timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{base_name}_{timestamp}.docx"

def process_template(data, output_filename, image_file=None):
    """
    Process a Word template using JSON data and return the document bytes.
    
    Args:
        data (dict): The JSON data to use in the template
        output_filename (str): The name of the output file
        image_file (UploadedFile, optional): The uploaded image file
    """
    # Path to your template
    template_path = "Mall 0.4.docx"
    
    try:
        # Load the template
        doc = DocxTemplate(template_path)
        
        # Handle image if provided
        if image_file is not None:
            # Read image and get dimensions
            image = Image.open(io.BytesIO(image_file.getvalue()))
            width, height = image.size
            
            # Calculate aspect ratio
            aspect_ratio = height / width
            
            # Base width in mm
            base_width = 40
            
            # Calculate height in mm maintaining aspect ratio
            height_mm = base_width * aspect_ratio
            
            # Check if image is in portrait format (height > width)
            if height <= width:
                st.warning("""
                Bilden bör vara i porträttformat (högre än bred). 
                Rekommenderat format är 3:4 eller 4:5.
                """)
            
            # Save the uploaded image to a temporary file
            temp_image_path = f"temp_image_{image_file.name}"
            with open(temp_image_path, "wb") as f:
                f.write(image_file.getvalue())
            
            # Create InlineImage object with both width and height
            data['profile_image'] = InlineImage(doc, temp_image_path, width=Mm(base_width), height=Mm(height_mm))
        else:
            data['profile_image'] = None
        
        # Lägg till 'assignments' för kompatibilitet med mallen
        assignments = data.get('assignment', [])
        # Kombinera roller till en sträng för varje assignment
        for assignment in assignments:
            if 'roles' in assignment and assignment['roles']:
                assignment['role'] = ', '.join(assignment['roles'])
        data['assignments'] = assignments
        # Lägg till 'educations' för kompatibilitet med mallen
        data['educations'] = data.get('educations', [])
        # Render the template with the provided context
        doc.render(data)
        
        # Save to a temporary file and read bytes
        temp_path = f"temp_{output_filename}"
        doc.save(temp_path)
        
        # Clean up temporary image file (after doc.save!)
        if image_file is not None:
            os.remove(temp_image_path)
        
        with open(temp_path, 'rb') as file:
            doc_bytes = file.read()
        
        # Clean up temporary file
        os.remove(temp_path)
        
        return doc_bytes
        
    except Exception as e:
        st.error(f"Fel vid bearbetning av mall: {str(e)}")
        return None

st.title("Konsultprofil Generator")

# Add Claude AI guidance section
st.markdown("""
### Steg 1: Skapa din konsultprofil med Claude AI
Innan du börjar redigera din profil i denna app, behöver du först skapa en grundläggande profil med hjälp av Claude AI. 
Detta hjälper dig att:
- Analysera din LinkedIn-profil
- Utvärdera tidigare konsultprofiler
- Skapa en strukturerad JSON-fil med all nödvändig information

1. Gå till [Claude AI-projektet](https://claude.ai/project/0196cdc8-e6ff-73d0-aff6-38ac9e6f57af)
2. Följ instruktionerna för att skapa din profil
3. Ladda ner den genererade JSON-filen
4. Fortsätt till steg 2 nedan för att redigera och finjustera din profil

---
""")

# File upload section
st.subheader("Steg 2: Ladda upp filer")
st.markdown("""
För att skapa din konsultprofil behöver du ladda upp två filer:
1. En JSON-fil med din profilinformation
2. En profilbild i porträttformat
""")

# Create two columns for file uploaders
col1, col2 = st.columns(2)

with col1:
    st.markdown("**JSON-fil med profilinformation**")
    uploaded_file = st.file_uploader("Välj JSON-fil", type=['json'], key="json_upload")

with col2:
    st.markdown("**Profilbild**")
    st.markdown("""
    **Viktigt om profilbilden:**
    - Bilden ska vara i porträttformat (högre än bred)
    - Rekommenderade proportioner: 3:4 eller 4:5
    - Stöds format: PNG, JPG, JPEG, GIF
    - Bilden kommer att visas i Word-dokumentet med en bredd på 40mm
    """)
    image_file = st.file_uploader("Välj profilbild", type=['png', 'jpg', 'jpeg', 'gif'], key="profile_image")

if uploaded_file is not None:
    # Read the uploaded file
    content = uploaded_file.getvalue().decode("utf-8")
    try:
        data = json.loads(content)
        
        # Display and edit the data
        st.subheader("Steg 3: Redigera din profil")
        
        # Basic information
        data['name'] = st.text_input("Namn", value=data.get('name', ''))
        data['slogan'] = st.text_input("Slogan", value=data.get('slogan', ''))
        data['summary'] = st.text_area("Sammanfattning", value=data.get('summary', ''), height=150)
        
        # Objectives (för kompatibilitet med mallen)
        data['objectives'] = st.text_area("Mål/Objectives", value=data.get('objectives', ''), height=100)
        
        # Expertise
        st.subheader("Expertis")
        expertise = data.get('expertise', [])
        
        # Add new expertise button
        if st.button("Lägg till expertis"):
            expertise.append("")
        
        for i, exp in enumerate(expertise):
            col1, col2 = st.columns([3, 1])
            with col1:
                expertise[i] = st.text_input(f"Expertis {i+1}", value=exp, key=f"exp_{i}")
            with col2:
                if st.button(f"Ta bort {i+1}", key=f"remove_exp_{i}"):
                    expertise.pop(i)
                    st.rerun()
        data['expertise'] = expertise

        # Assignments
        st.subheader("Uppdrag")
        assignments = data.get('assignment', [])
        
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
            
            # Roles field
            roles = assignment.get('roles', [])
            st.write("Roller:")
            if st.button(f"Lägg till roll för uppdrag {i+1}", key=f"add_role_{i}"):
                roles.append("")
            
            for j, role in enumerate(roles):
                col1, col2 = st.columns([3, 1])
                with col1:
                    roles[j] = st.text_input(f"Roll {j+1} för uppdrag {i+1}", value=role, key=f"role_{i}_{j}")
                with col2:
                    if st.button(f"Ta bort roll {j+1}", key=f"remove_role_{i}_{j}"):
                        roles.pop(j)
                        st.rerun()
            assignment['roles'] = roles
            
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
        
        # Technologies
        st.write("**Teknologier**")
        technologies = data.get('technologies', [])
        if st.button("Lägg till teknologi"):
            technologies.append("")
        
        for i, tech in enumerate(technologies):
            col1, col2 = st.columns([3, 1])
            with col1:
                technologies[i] = st.text_input(f"Teknologi {i+1}", value=tech, key=f"tech_{i}")
            with col2:
                if st.button(f"Ta bort {i+1}", key=f"remove_tech_{i}"):
                    technologies.pop(i)
                    st.rerun()
        data['technologies'] = technologies

        # Methods
        st.write("**Metoder**")
        methods = data.get('methods', [])
        if st.button("Lägg till metod"):
            methods.append("")
        
        for i, method in enumerate(methods):
            col1, col2 = st.columns([3, 1])
            with col1:
                methods[i] = st.text_input(f"Metod {i+1}", value=method, key=f"method_{i}")
            with col2:
                if st.button(f"Ta bort {i+1}", key=f"remove_method_{i}"):
                    methods.pop(i)
                    st.rerun()
        data['methods'] = methods

        # Tools
        st.write("**Verktyg**")
        tools = data.get('tools', [])
        if st.button("Lägg till verktyg"):
            tools.append("")
        
        for i, tool in enumerate(tools):
            col1, col2 = st.columns([3, 1])
            with col1:
                tools[i] = st.text_input(f"Verktyg {i+1}", value=tool, key=f"tool_{i}")
            with col2:
                if st.button(f"Ta bort {i+1}", key=f"remove_tool_{i}"):
                    tools.pop(i)
                    st.rerun()
        data['tools'] = tools

        # Languages
        st.subheader("Språk")
        languages = data.get('languages', [
            {"language": "Svenska", "level": "Modersmål"},
            {"language": "Engelska", "level": "Flytande"},
            {"language": "Spanska", "level": "Grundläggande"}
        ])
        
        if st.button("Lägg till språk"):
            languages.append({"language": "", "level": ""})
        
        for i, lang in enumerate(languages):
            col1, col2, col3 = st.columns([2, 2, 1])
            with col1:
                lang['language'] = st.text_input(f"Språk {i+1}", value=lang.get('language', ''), key=f"lang_{i}")
            with col2:
                lang['level'] = st.text_input(f"Nivå {i+1}", value=lang.get('level', ''), key=f"level_{i}")
            with col3:
                if st.button(f"Ta bort {i+1}", key=f"remove_lang_{i}"):
                    languages.pop(i)
                    st.rerun()
        data['languages'] = languages

        # Education
        st.subheader("Utbildning")
        educations = data.get('educations', [])
        
        if st.button("Lägg till utbildning"):
            educations.append({
                "institution": "",
                "focus": "",
                "period": ""
            })
        
        for i, edu in enumerate(educations):
            st.markdown(f"### Utbildning {i+1}")
            col1, col2, col3 = st.columns([2, 2, 1])
            with col1:
                edu['institution'] = st.text_input(f"Institution {i+1}", value=edu.get('institution', ''), key=f"inst_{i}")
            with col2:
                edu['focus'] = st.text_input(f"Inriktning {i+1}", value=edu.get('focus', ''), key=f"focus_{i}")
                edu['period'] = st.text_input(f"Period {i+1}", value=edu.get('period', ''), key=f"edu_period_{i}")
            with col3:
                if st.button(f"Ta bort {i+1}", key=f"remove_edu_{i}"):
                    educations.pop(i)
                    st.rerun()
        
        data['educations'] = educations

        # Certifications and Training
        st.subheader("Certifieringar och utbildningar")
        certifications = data.get('certifications', [])
        
        if st.button("Lägg till certifiering/utbildning"):
            certifications.append("")
        
        for i, cert in enumerate(certifications):
            col1, col2 = st.columns([3, 1])
            with col1:
                certifications[i] = st.text_input(f"Certifiering/Utbildning {i+1}", value=cert, key=f"cert_{i}")
            with col2:
                if st.button(f"Ta bort {i+1}", key=f"remove_cert_{i}"):
                    certifications.pop(i)
                    st.rerun()
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
                doc_bytes = process_template(data, output_filename, image_file)
                
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