import os
import re

RAW_DIR = "data/rfc_raw/"
OUT_DIR = "data/rfc_clean/"

os.makedirs(OUT_DIR, exist_ok=True)

def clean_text(text):
    # Remove page headers like "RFC 791 1981"
    text = re.sub(r"RFC\s+\d+.*\n", "", text)

    # Remove page numbers
    text = re.sub(r"\n\s*\d+\s*\n", "\n", text)

    # Remove form feed
    text = text.replace("\f", "")

    # Remove multiple blank lines
    text = re.sub(r"\n\s*\n", "\n", text)

    return text.strip()

for fname in os.listdir(RAW_DIR):
    if fname.endswith(".txt"):
        with open(RAW_DIR + fname, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read()

        clean = clean_text(text)

        with open(OUT_DIR + fname, "w", encoding="utf-8") as f:
            f.write(clean)

print("✔ Cleaned all RFC files!")
