# agents/retriever.py
from core.embedder import TextEmbedder
import faiss
import numpy as np
import os

class RetrieverAgent:
    def __init__(self):
        # 1. Khởi tạo Embedder
        self.embedder = TextEmbedder() 
        
        # 2. Load FAISS Index (RFC Knowledge)
        self.index_path = "data/rfc_index.faiss"
        self.chunks_path = "data/rfc_chunks.npy"
        
        if os.path.exists(self.index_path) and os.path.exists(self.chunks_path):
            self.index = faiss.read_index(self.index_path)
            self.chunks = np.load(self.chunks_path, allow_pickle=True)
            print("✔ [Agent 2] Đã load Database RFC.")
        else:
            self.index = None
            print("⚠️ [Agent 2] Chưa tìm thấy Database RFC. Chế độ RAG bị tắt.")

        # 3. Load Templates Map
        self.template_map = {
            "create_vlan": "vlan.j2",
            "setup_ospf_advanced": "ospf.j2",
            "advanced_acl": "acl.j2",
            "nat_static": "nat.j2",
            "nat_dynamic": "nat.j2",
            "set_interface_ip": "interface_ip.j2",
        }

    def retrieve(self, intent_data, user_query):
        print(f"📚 [Agent 2] Đang tìm kiếm tài nguyên...")
        intent = intent_data["intent"]
        
        # --- A. Lấy Template ---
        template_file = self.template_map.get(intent)
        
        # --- B. Tìm kiếm Semantic (RAG) ---
        rfc_context = ""
        if self.index:
            # Dùng Embedder để mã hóa câu hỏi người dùng
            query_vector = self.embedder.embed(user_query)
            query_vector = np.array([query_vector]).astype('float32')
            
            # Search FAISS
            distances, indices = self.index.search(query_vector, k=2)
            
            results = []
            for idx in indices[0]:
                if idx < len(self.chunks):
                    results.append(self.chunks[idx])
            
            rfc_context = "\n---\n".join(results)

        return {
            "template_file": template_file,
            "rfc_context": rfc_context
        }