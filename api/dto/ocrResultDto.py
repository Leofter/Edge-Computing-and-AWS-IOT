from pydantic import BaseModel
from typing import Optional


class OCRResultDTO(BaseModel):
    rec_text: str
    rec_score: float
    input_path: Optional[str] = None
