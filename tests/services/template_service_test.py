import io
from typing import List
from reportlab.pdfgen import canvas
import pytest
from reportlab.lib.pagesizes import letter
from templates.services.template_service import TemplateService
from templates.models.template import Template

@pytest.fixture
def template_service():
    return TemplateService()

@pytest.fixture
def create_pdf():
    def _create_pdf(text_lines: List[str]) -> bytes:
        """Create a PDF file from a list of text lines."""
        if not text_lines:
            raise ValueError("Text lines cannot be empty")
        # Create a PDF in memory
        pdf_buffer = io.BytesIO()
        c = canvas.Canvas(pdf_buffer, pagesize=letter)
        y = 750
        for line in text_lines:
            c.drawString(100, y, line)
            y -= 20
        c.showPage()
        c.save()
        pdf_bytes = pdf_buffer.getvalue()
        pdf_buffer.close()
        return pdf_bytes
    return _create_pdf

def test_does_template_contain_text(create_pdf, template_service):
    pdf_bytes = create_pdf(["Hello, World!", "Hey there!"])
    assert template_service.does_template_contain_text(["Hello, World!", "Hey there!"], Template(id=1, name="Test Template", pdf_file=pdf_bytes)) is True
    assert template_service.does_template_contain_text(["World, Hello!", "Hey there!"], Template(id=1, name="Test Template", pdf_file=pdf_bytes)) is False

def test_validate_template(create_pdf, template_service):
    pdf_bytes = create_pdf(TemplateService.FIELDS)
    pdf_bytes_invalid = create_pdf(TemplateService.FIELDS[:-1])  # Missing one field
    assert template_service.validate_template(Template(id=1, name="Test Template", pdf_file=pdf_bytes)) is True
    assert template_service.validate_template(Template(id=2, name="Invalid Template", pdf_file=pdf_bytes_invalid)) is False