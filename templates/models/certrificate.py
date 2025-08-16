from datetime import date
from pydantic import Base64Bytes
from sqlmodel import Field, SQLModel

class CertificateRequest(SQLModel):    
    template_id: int | None = Field(default=None, foreign_key="template.id", description="Template ID")
    student_name: str = Field(..., index=True, description="Student name.")
    degree: str = Field(..., index=True, description="Degree name.")
    institution: str = Field(..., index=True, description="Institution name.")
    issue_date: date = Field(..., description="Date of issue.")
    signature: str = Field(..., description="Signature of the authority.")

class Certificate(CertificateRequest, table=True):    
    id: int | None = Field(default=None, primary_key=True, description="Certificate ID")
    pdf_file: Base64Bytes | None = Field(description="PDF file content as bytes", nullable=True)