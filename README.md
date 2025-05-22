# Konsultprofiler

Detta projekt består av tre delar:
1. En Claude AI-applikation som hjälper till att skapa JSON-filer med konsultprofildata
2. Ett Python-program som använder JSON-filen för att generera Word-dokument baserat på en mall
3. En Streamlit-webbapplikation för att redigera konsultprofiler interaktivt

Detta projekt innehåller också instruktionsfilen `INSTRUCTION TO AI – GENERATE JSON.txt` som används som mall för att generera konsultprofiler via Claude AI.

## Installation

### 1. Installera `make` (första gången)
- **Windows:**
  - **Öppna PowerShell som administratör** (högerklicka på PowerShell och välj "Kör som administratör")
  - Navigera till projektkatalogen:
    ```powershell
    cd C:\sök\till\din\katalog\konsultprofiler
    ```
  - Installera via [Chocolatey](https://chocolatey.org/):
    ```powershell
    choco install make
    ```
  - Eller ladda ner från [GnuWin](http://gnuwin32.sourceforge.net/packages/make.htm)
- **Mac/Linux:**
  - `make` är oftast redan installerat.

### 2. Klona projektet och kör:
```sh
make all
```
Detta:
- Skapar en virtuell miljö
- Installerar alla beroenden
- Startar Streamlit-appen

### 3. Rensa miljön (om du får problem)
```sh
make stop
```
Tar bort `.venv`-mappen så du kan börja om.

## Utvecklarläge & Testa appen

### Starta appen i utvecklarläge
1. Öppna en terminal i projektmappen
2. Kör:
   ```sh
   streamlit run src/konsultprofiler/app.py
   ```
   (eller kör `make all` för att automatiskt skapa miljö och starta appen)
3. Öppna webbläsaren på adressen som visas (vanligtvis http://localhost:8501)

### Testa JSON och konsultfoto
1. **Ladda upp en JSON-fil** (skapa via Claude AI eller ladda ner ett exempel)
2. **Ladda upp ett konsultfoto** (porträttformat, t.ex. 3:4)
3. Redigera profilinformationen direkt i appen
4. Klicka på "Generera Word-dokument" för att testa att både data och foto hamnar rätt i dokumentet
5. Ladda ner och öppna Word-filen för att kontrollera resultatet

> **Tips:** Du behöver aldrig redigera JSON-filen manuellt – all redigering sker i webbläsaren!

### Felsökning
- Om du får problem med miljön eller beroenden:
  ```sh
  make stop
  make all
  ```
  Detta rensar och bygger om allt från början.

## Användning (översikt)

### Word-dokument generering
1. Skapa en JSON-fil med konsultprofildata via Claude AI (se länk i appen)
2. Kör programmet:
   ```sh
   python src/konsultprofiler/template_processor.py
   ```
3. Följ instruktionerna i programmet

### Streamlit webbapplikation
1. Starta appen (eller kör `make all`):
   ```sh
   streamlit run src/konsultprofiler/app.py
   ```
2. Ladda upp din JSON-fil och profilbild i appen  
   _(Du kan skapa och redigera all information direkt i webbläsaren – du behöver inte öppna eller redigera JSON-filer manuellt!)_
3. Redigera och ladda ner din konsultprofil

## Filstruktur

- `src/konsultprofiler/` - Python-koden
- `Mall 0.2.docx` - Word-mall
- `INSTRUCTION TO AI – GENERATE JSON.txt` - Mall för Claude AI
- `pyproject.toml` - Projektkonfiguration
- `Makefile` - Automatiserar installation och körning 