import os
import re

RFC_DIR = "data/rfc_clean/"   # thư mục chứa các file txt RFC đã làm sạch

# ---- STEP 1: Load toàn bộ RFC vào danh sách chunk ----
def load_rfc_chunks():
    chunks = []
    index = []   # lưu: (filename, chunk_text)

    for fname in os.listdir(RFC_DIR):
        if fname.endswith(".txt"):
            path = os.path.join(RFC_DIR, fname)
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                text = f.read()

            # Chia theo đoạn (2–6 dòng / chunk)
            raw_chunks = text.split("\n\n")  # chia theo đoạn rỗng

            for ch in raw_chunks:
                cleaned = ch.strip()
                if len(cleaned) > 50:   # bỏ đoạn quá ngắn
                    chunks.append(cleaned)
                    index.append((fname, cleaned))

    return chunks, index


RFC_CHUNKS, RFC_INDEX = load_rfc_chunks()


# ---- STEP 2: Tìm chunk phù hợp nhất theo keyword ----
def score_chunk(question, chunk):
    q = question.lower()
    c = chunk.lower()

    score = 0

    for word in q.split():
        if word in c:
            score += 1

    return score


def search_rfc(question):
    best_score = 0
    best_chunk = None
    best_file = None

    for (fname, chunk) in RFC_INDEX:
        s = score_chunk(question, chunk)
        if s > best_score:
            best_score = s
            best_chunk = chunk
            best_file = fname

    if best_chunk:
        return best_file, best_chunk

    return None, None
