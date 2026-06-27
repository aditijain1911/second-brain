from sqlmodel import SQLModel, Field, create_engine, Session, select
from typing import Optional
from datetime import datetime

class Document(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    url: str
    title: str
    text: str
    timestamp: datetime
    source_type: str = "browser"

engine = create_engine("sqlite:///memories.db")

def create_db():
    SQLModel.metadata.create_all(engine)

def save_document(payload):
    with Session(engine) as session:
        doc = Document(
            url=payload.url,
            title=payload.title,
            text=payload.text,
            timestamp=payload.timestamp,
            source_type=payload.source_type
        )
        session.add(doc)
        session.commit()