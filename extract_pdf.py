#!/usr/bin/env python3
import sys
try:
    import pdfplumber
    has_pdfplumber = True
except ImportError:
    has_pdfplumber = False
    try:
        import PyPDF2
        has_pypdf2 = True
    except ImportError:
        has_pypdf2 = False

if has_pdfplumber:
    with pdfplumber.open('agpia_2009.pdf') as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text() + "\n"
        print(text)
elif has_pypdf2:
    with open('agpia_2009.pdf', 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        print(text)
else:
    print("ERROR: No PDF library available. Please install pdfplumber or PyPDF2", file=sys.stderr)
    sys.exit(1)

