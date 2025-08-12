from pydantic import BaseModel, Field
from typing import Optional

class Template(BaseModel):
    id: int
    name: str
    pdf_file: bytes = Field(..., description="PDF file content as bytes")