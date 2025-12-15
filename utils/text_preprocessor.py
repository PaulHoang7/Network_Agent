import re
import os
from typing import List, Optional, Set
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class TextPreprocessor:
    """
    Preprocesses text for Network Automation domain.
    Preserves IP addresses, CIDR, Interface names, and CLI commands.
    """

    def __init__(
        self,
        lowercase: bool = True,
        remove_special: bool = True,
        stopwords_file: Optional[str] = None
    ):
        self.lowercase = lowercase
        self.remove_special = remove_special

        # Default stopwords (Generic English)
        # LƯU Ý: Đã loại bỏ 'in', 'out', 'to', 'from', 'on' vì quan trọng trong ACL/Interface
        self.default_stopwords = {
            'the', 'a', 'an', 'and', 'or', 'but', 
            'is', 'are', 'was', 'were', 'be', 'been',
            'being', 'have', 'has', 'had', 'do', 'does', 'did', 
            'will', 'would', 'should', 'could', 'may', 'might', 'must', 'can',
            'this', 'that', 'these', 'those', 
            'i', 'you', 'he', 'she', 'it', 'we', 'they'
        }

        self.stopwords = self._load_stopwords(stopwords_file)

    def _load_stopwords(self, stopwords_file: Optional[str]) -> Set[str]:
        if stopwords_file is None:
            return self.default_stopwords
            
        try:
            with open(stopwords_file, 'r', encoding='utf-8') as f:
                stopwords = {line.strip().lower() for line in f if line.strip() and not line.startswith('#')}
            return stopwords
        except Exception as e:
            logger.warning(f"Failed to load stopwords: {e}")
            return self.default_stopwords

    def clean_text(self, text: str) -> str:
        """
        Clean text while preserving Network terms (IP, CIDR, Interface).
        """
        if not text:
            return ""

        cleaned = text.strip()

        if self.lowercase:
            cleaned = cleaned.lower()

        if self.remove_special:
            # GIỮ LẠI: / (interface/cidr), . (ip), : (ipv6/mac), * (wildcard)
            # Regex: Giữ lại word char, space, và các ký tự đặc biệt mạng
            cleaned = re.sub(r'[^\w\s\-.,;:()/*]', ' ', cleaned)
            
            # Xóa khoảng trắng thừa
            cleaned = re.sub(r'\s+', ' ', cleaned)

        return cleaned.strip()

    def remove_stopwords(self, text: str) -> str:
        words = text.split()
        filtered = [w for w in words if w.lower() not in self.stopwords]
        return ' '.join(filtered)

    def preprocess(
        self,
        text: str,
        remove_stops: bool = False, # Mặc định False để an toàn cho lệnh CLI
        min_length: int = 1         # Mặc định 1 để giữ lại số '1', '0'
    ) -> str:
        if not text:
            return ""

        processed = self.clean_text(text)

        if remove_stops:
            processed = self.remove_stopwords(processed)

        words = processed.split()
        words = [w for w in words if len(w) >= min_length]
        processed = ' '.join(words)

        return processed

    def preprocess_batch(self, texts: List[str], remove_stops: bool = False) -> List[str]:
        return [self.preprocess(text, remove_stops) for text in texts]