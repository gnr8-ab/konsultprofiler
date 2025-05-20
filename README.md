# Konsultprofiler

Detta projekt består av tre delar:
1. En Claude AI-applikation som hjälper till att skapa JSON-filer med konsultprofildata (se länk nedan)
2. Ett Python-program som använder JSON-filen för att generera Word-dokument baserat på en mall
3. En Streamlit-webbapplikation för att redigera konsultprofiler interaktivt

Detta projekt innehåller också instruktionsfilen `INSTRUCTION TO AI – GENERATE JSON.txt` som används som mall för att generera konsultprofiler via Claude AI.

## Installation

### Windows
1. Installera Python 3.x om du inte redan har det
2. Installera uv:
```bash
pip install --user uv
```
3. Skapa och aktivera en virtuell miljö:
```bash
uv venv
.venv\Scripts\activate
```
4. Installera beroenden:
```bash
uv pip install docxtpl streamlit
```

### Mac
1. Installera Python 3.x om du inte redan har det
2. Installera uv:
```bash
pip install --user uv
```
3. Skapa och aktivera en virtuell miljö:
```bash
uv venv
source .venv/bin/activate
```
4. Installera beroenden:
```bash
uv pip install docxtpl streamlit
```

## Användning

### Word-dokument generering
1. Skapa en JSON-fil med konsultprofildata genom att använda Claude AI-applikationen på: https://claude.ai/project/0196cdc8-e6ff-73d0-aff6-38ac9e6f57af

2. Kör Python-programmet:
```bash
python template_processor.py
```

3. Följ instruktionerna i programmet:
   - Välj din JSON-fil
   - Välj var du vill spara det genererade Word-dokumentet

### Streamlit webbapplikation
1. Starta Streamlit-appen:
```bash
streamlit run app.py
```

2. Öppna webbläsaren på den angivna adressen (vanligtvis http://localhost:8501)
3. Ladda upp en JSON-fil med konsultprofil
4. Redigera informationen i formuläret
5. Spara och ladda ner den uppdaterade JSON-filen

## Filstruktur

- `template_processor.py` - Huvudprogrammet som genererar dokument
- `app.py` - Streamlit-webbapplikationen för att redigera profiler
- `Mall 0.2.docx` - Word-mall som används som bas för genereringen
- `INSTRUCTION TO AI – GENERATE JSON.txt` - Mall för att generera konsultprofiler via Claude AI
- `pyproject.toml` - Projektkonfiguration och beroenden
- JSON-fil - Innehåller data som ska användas i dokumentet (skapas via Claude AI) 