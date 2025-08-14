import io
from annotated_types import doc
import fitz  
from templates.models import template
from templates.models.template import Template
from typing import List, Optional, Dict
from templates.db.sqlite import SessionDep
from sqlmodel import Field, Session, SQLModel, create_engine, select

class InvalidTemplateException(Exception):
    pass

class TemplateService:
    
    FIELDS = ['FULANO_DE_TAL', 'DEGREE', 'INSTITUTION', 'SIGNATURE', 'DATE']
    
    def __init__(self, session: SessionDep):
        self.session = session
   
    def open_template_doc(self, template: Template):
        pdf_stream = io.BytesIO(template.pdf_file)
        return fitz.open(stream=pdf_stream, filetype="pdf")
        
    def does_template_contain_text(self, text: List[str], template: Template) -> bool:
        doc = self.open_template_doc(template)
        try:
            for page_num, page in enumerate(doc, start=1):
                if all(t in page.get_text() for t in text):
                    continue
                else:
                    return False
        finally:
            doc.close()
        return True

    def validate_template(self, template: Template) -> bool:
        return self.does_template_contain_text(TemplateService.FIELDS, template)

    def replace_template_fields(self, template: Template, replacements: Dict) -> Template:
        doc = self.open_template_doc(template)
        try:
            for page in doc:
                for field, value in replacements.items():
                    hits = page.search_for(field)
                    for rect in hits:
                       page.add_redact_annot(rect, value, fontname="TiRo", fontsize=14,
                           align=fitz.TEXT_ALIGN_CENTER)
                page.apply_redactions(images=fitz.PDF_REDACT_IMAGE_NONE)
            new_pdf_stream = io.BytesIO()
            doc.save(new_pdf_stream)
            template.pdf_file = new_pdf_stream.getvalue()
            return template
        finally:
            doc.close()
      
    def create_template(self, template: Template):
        if not self.validate_template(template):
            raise InvalidTemplateException("Invalid template.")
        self.session.add(template)
        self.session.commit()
        self.session.refresh(template)
        return template
    
    def get_template(self, template_id: int) -> Optional[Template]:
        return self.session.get(Template, template_id)
      
    def update_template(self, template_id: int, template: Template) -> Optional[Template]:
        template = self.session.get(Template, template_id)
        if not template:
            return None
        self.session.merge(template)
        self.session.commit()
        return template
  
    def delete_template(self, template_id: int) -> Optional[Template]:
        template = self.session.get(Template, template_id)
        if not template:
            return None
        self.session.delete(template)
        self.session.commit()
        return template
    
    def get_templates(self,  offset: int = 0, limit: int = 10):
        return self.session.exec(select(Template).offset(offset).limit(limit)).all()
