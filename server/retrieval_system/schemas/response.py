from typing import List, Optional

from pydantic import BaseModel


class FaissRespone(BaseModel):
    response: List[str]
    distances: List[float]
