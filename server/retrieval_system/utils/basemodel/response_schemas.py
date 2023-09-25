from typing import Dict, List, Union

from pydantic import BaseModel


class QueryContent(BaseModel):
    text_descriptions: Union[List[Dict], None]
    text_ocr: Union[str, None]
    text_asr: Union[str, None]
    text_asr_method: Union[str, None]
    image: Union[Dict, None]
    object_tags: Union[List[Dict], None]
    top_k: Union[int, None]


class ExportListItem(BaseModel):
    video_id: str
    keyframe_id: str
