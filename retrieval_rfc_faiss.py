import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import os

# Cấu hình đường dẫn
INDEX = "data/rfc_index.faiss"
CHUNKS = "data/rfc_chunks.npy"
MAP = "data/rfc_map.txt"

# 1. Load Model
print("Bắt đầu load model...")
model = SentenceTransformer("all-MiniLM-L6-v2")
print("✔ Model loaded!")

# 2. Load Data (Index, Chunks, Mapping)
# Bạn cần load Chunks dù Index có load được hay không, vì hàm search cần dùng nó để hiển thị text.
try:
    print("📦 Loading resources...")
    
    # Load Index
    index = faiss.read_index(INDEX)
    
    # Load Chunks (Sửa lỗi: Phải load cái này ra biến global)
    chunks = np.load(CHUNKS, allow_pickle=True)
    
    # Load Mapping
    with open(MAP, "r", encoding="utf-8") as f:
        mapping = f.read().splitlines()
        
    print("✔ Tất cả dữ liệu đã được load thành công!")

except Exception as e:
    print(f"❌ ERROR loading resources: {e}")
    # Nếu thiếu file quan trọng thì dừng chương trình
    exit()

# 3. Định nghĩa hàm Search
def semantic_search(question, top_k=3):
    # Encode câu hỏi
    q_emb = model.encode([question], convert_to_numpy=True)
    
    # Search trong FAISS
    distances, idx = index.search(q_emb, top_k)
    
    results = []
    for i in range(top_k):
        # Lấy index thực tế
        result_index = idx[0][i]
        
        # Kiểm tra xem index có hợp lệ không (đề phòng lỗi out of bound)
        if result_index < len(chunks):
            chunk_text = chunks[result_index]
            file_name = mapping[result_index] if result_index < len(mapping) else "Unknown"
            score = distances[0][i]
            results.append((file_name, chunk_text, float(score)))
    
    return results

# 4. Main Execution (Phần bạn muốn thêm vào)
# Đặt ở cuối file
if __name__ == "__main__":
    print("\n--- TEST SEARCH ---")
    query = "How does TCP handshake work?"
    print(f"🔍 Searching for: '{query}'\n")
    
    results = semantic_search(query)
    
    for r in results:
        print("-" * 30)
        print(f"File: {r[0]}")
        print(f"Score: {r[2]:.4f}") # Format số thập phân cho đẹp
        print(f"Chunk: {r[1][:300]} ...") # In 300 ký tự đầu