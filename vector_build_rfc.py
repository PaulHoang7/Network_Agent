import os
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

RFC_DIR = "data/rfc_clean/"
OUT_INDEX = "data/rfc_index.faiss"
OUT_CHUNKS = "data/rfc_chunks.npy"
OUT_MAP = "data/rfc_map.txt"

model = SentenceTransformer("all-MiniLM-L6-v2")

def load_rfc_chunks():
    chunks = []
    mapping = []  # (file, chunk_text)

    for fname in os.listdir(RFC_DIR):
        if fname.endswith(".txt"):
            with open(os.path.join(RFC_DIR, fname), "r", encoding="utf-8") as f:
                text = f.read()

            blocks = text.split("\n\n")
            for b in blocks:
                b = b.strip()
                if len(b) > 60:
                    chunks.append(b)
                    mapping.append(fname)
    return chunks, mapping

print("📥 Loading RFC files...")
chunks, mapping = load_rfc_chunks()

print(f"✔ Loaded {len(chunks)} chunks")

print("🔢 Encoding embeddings...")
embeddings = model.encode(chunks, convert_to_numpy=True)

print("📚 Saving mapping...")
with open(OUT_MAP, "w", encoding="utf-8") as f:
    for m in mapping:
        f.write(m + "\n")

print("💾 Saving chunks...")
np.save(OUT_CHUNKS, chunks, allow_pickle=True)

print("📦 Building FAISS index...")
dim = embeddings.shape[1]
index = faiss.IndexFlatL2(dim)
index.add(embeddings)

faiss.write_index(index, OUT_INDEX)
print("🎉 FAISS index created!")
