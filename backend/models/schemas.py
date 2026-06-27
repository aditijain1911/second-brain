from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class IngestPayload(BaseModel):
    url: str
    title: str
    text: str
    timestamp: datetime
    source_type: str = "browser"  # browser | pdf | note | clipboard
    tags: Optional[list[str]] = []