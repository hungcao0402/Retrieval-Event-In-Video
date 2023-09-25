from typing import List, Optional

from pydantic import BaseModel


class TextQuery(BaseModel):
    text: str
    top_k: int = 100


class TextQueryContent(BaseModel):
    clip_queries: Optional[List[TextQuery]] = None
    ocr_query: Optional[TextQuery] = None
    asr_query: Optional[TextQuery] = None
    positive_frames: List[str]
    negative_frames: List[str]
    final_top_k: int
