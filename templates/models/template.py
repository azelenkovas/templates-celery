from pydantic import Base64Bytes, Field, BaseModel
from typing import Optional


class Template(BaseModel):
    id: int = Field(..., description="Template ID")
    name: str = Field(..., description="Template name.")
    pdf_file: Base64Bytes = Field(..., description="PDF file content as bytes")
