from tempfile import template
import pytest
from tests.base_fixtures import create_pdf
from templates.services.template_service import TemplateService
from templates.models.template import Template
import base64
from unittest.mock import MagicMock

@pytest.fixture
def template_service():
    session_mock = MagicMock()
    return TemplateService(session=session_mock)

def test_does_template_contain_text(create_pdf, template_service):
    pdf_bytes_base64 = create_pdf(["Hello, World!", "Hey there!"])
    assert template_service.does_template_contain_text(["Hello, World!", "Hey there!"], Template(id=1, name="Test Template", pdf_file=pdf_bytes_base64)) is True
    assert template_service.does_template_contain_text(["World, Hello!", "Hey there!"], Template(id=1, name="Test Template", pdf_file=pdf_bytes_base64)) is False

def test_validate_template(create_pdf, template_service):
    pdf_bytes_base64 = create_pdf(TemplateService.FIELDS)
    pdf_bytes_invalid_base64 = create_pdf(TemplateService.FIELDS[:-1])  # Missing one field
    assert template_service.validate_template(Template(id=1, name="Test Template", pdf_file=pdf_bytes_base64)) is True
    assert template_service.validate_template(Template(id=2, name="Invalid Template", pdf_file=pdf_bytes_invalid_base64)) is False
    
def test_replace_template_fields(create_pdf, template_service):
    pdf_bytes_base64 = create_pdf(TemplateService.FIELDS)
    template = Template(id=1, name="Test Template", pdf_file=pdf_bytes_base64)
    fields = {
        "FULANO_DE_TAL": "John Doe",
        "DEGREE": "PhD in Testing",
        "INSTITUTION": "University of Testing",
        "SIGNATURE": "John Doe",
        "DATE": "2023-01-01"
    }
    template = template_service.replace_template_fields(template, fields)
    assert all(template_service.does_template_contain_text([v], template) is True for v in list(fields.values()))
    assert all(template_service.does_template_contain_text([v], template) is False for v in list(fields.keys()))
