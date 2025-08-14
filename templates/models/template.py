from pydantic import Base64Bytes
from sqlmodel import Field, SQLModel

class Template(SQLModel, table=True):    
    id: int | None = Field(default=None, primary_key=True, description="Template ID")
    name: str = Field(index=True, description="Template name.")  
    description: str = Field(description="Template description.")
    pdf_file: Base64Bytes = Field(..., description="PDF file content as bytes")
