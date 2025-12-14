import os

IN_DIR = "data/rfc_clean/"
OUT_FILE = "data/rfc_knowledge.txt"

with open(OUT_FILE, "w", encoding="utf-8") as out:
    for fname in os.listdir(IN_DIR):
        if fname.endswith(".txt"):
            with open(IN_DIR + fname, "r", encoding="utf-8") as f:
                out.write(f"\n\n[FILE: {fname}]\n")
                out.write(f.read())

print("✔ Combined all RFC into rfc_knowledge.txt")
