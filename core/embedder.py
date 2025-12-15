import torch
from sentence_transformers import SentenceTransformer
from typing import List, Union

class TextEmbedder:
    """
    Class quản lý việc chuyển đổi văn bản sang Vector (Embedding).
    Model mặc định: all-MiniLM-L6-v2 (Nhẹ, nhanh, phổ biến cho RAG)
    """

    def __init__(
        self,
        model_name: str = "all-MiniLM-L6-v2", # Dùng model này cho đồng bộ với file tạo index cũ của bạn
        device: str = None
    ):
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        print(f"📦 [Embedder] Loading model '{model_name}' on {self.device}...")
        self.model = SentenceTransformer(model_name, device=self.device)

    def embed(self, text: Union[str, List[str]]) -> List[float]:
        """
        Chuyển text thành vector list
        """
        # Nếu là string đơn, chuyển thành list để xử lý chung
        is_single = isinstance(text, str)
        texts = [text] if is_single else text

        # Preprocessing đơn giản (lowercase)
        texts = [t.lower().strip() for t in texts]

        with torch.no_grad():
            embeddings = self.model.encode(
                texts,
                convert_to_tensor=True,
                show_progress_bar=False,
                normalize_embeddings=True
            )

        result = embeddings.cpu().tolist()
        return result[0] if is_single else result
    
    def get_dimension(self) -> int:
        return self.model.get_sentence_embedding_dimension()