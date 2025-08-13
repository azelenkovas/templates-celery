import pytest
from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import io
from typing import List
from reportlab.lib.pagesizes import letter


@pytest.fixture
def fixed_datetime():
    return datetime.fromisoformat('2021-02-03T04:05:06.123456+00:00')

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
        #c.showPage()
        c.save()
        pdf_bytes = pdf_buffer.getvalue()
        pdf_buffer.close()
        return pdf_bytes
    return _create_pdf