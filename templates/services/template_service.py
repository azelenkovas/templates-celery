import io
import fitz  
from templates.models.template import Template
from typing import List, Optional

class TemplateService:
    
    FIELDS = ['FULANO_DE_TAL', 'DEGREE', 'INSTITUTION', 'SIGNATURE', 'DATE']
    
    def __init__(self):
        pass

    def does_template_contain_text(self, text: List[str], template: Template) -> bool:
        pdf_stream = io.BytesIO(template.pdf_file)
        doc = fitz.open(stream=pdf_stream, filetype="pdf")
        for page_num, page in enumerate(doc, start=1):
            if all(t in page.get_text() for t in text):
                continue
            else:
                return False
        return True

    def validate_template(self, template: Template) -> bool:
        return self.does_template_contain_text(TemplateService.FIELDS, template)

    def create_template(self, template: Template):
        pass

    def get_template(self, template_id: int) -> Optional[Template]:
        pass

    def update_template(self, template_id: int, template: Template):
        pass

    def delete_template(self, template_id: int):
        pass
    