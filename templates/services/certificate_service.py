import io
from annotated_types import doc
import fitz  
from templates.models import template
from templates.models.template import Template
from typing import List, Optional, Dict
from templates.db.postgresql import SessionDep
from sqlmodel import Field, Session, SQLModel, create_engine, select
from templates.services.template_service import TemplateService
from templates.models.certrificate import CertificateRequest, Certificate
import logging
class TemplateNotFound(Exception):
    pass

class CertificateNotFound(Exception):
    pass

class CertificateService:
    
    def __init__(self, session: SessionDep):
        self.session = session
        self.template_service = TemplateService(session)
    
    def request_certificate(self, certificate_request: CertificateRequest) -> Certificate:
        logging.info(f"Requesting certificate for template {certificate_request.template_id} student {certificate_request.student_name}...")
        template = self.template_service.get_template(certificate_request.template_id)
        if not template:
            raise TemplateNotFound("Template not found.")
        certificate = Certificate(**(certificate_request.model_dump()))
        self.session.add(certificate)
        self.session.commit()
        self.session.refresh(certificate)
        logging.info(f"Certificate requested: {certificate.id} for template {template.id} student {certificate.student_name}")
        return certificate
    
    def issue_certificate(self, certificate_id: int):
        logging.info(f"Issuing certificate: {certificate_id}...")
        certificate = self.session.get(Certificate, certificate_id)
        if not certificate:
            raise CertificateNotFound("Certificate not found.")
        template = self.template_service.get_template(certificate.template_id)
        if not template:
            raise TemplateNotFound("Template not found.")
        print(template.model_dump_json())
        self.template_service.replace_template_fields(template, {
            "FULANO_DE_TAL": certificate.student_name,
            "DEGREE": certificate.degree,
            "INSTITUTION": certificate.institution,
            "SIGNATURE": certificate.signature,
            "DATE": certificate.issue_date.isoformat()
        })
        certificate.pdf_file = template.pdf_file
        self.session.merge(certificate)
        self.session.commit()
        self.session.refresh(certificate)
        logging.info(f"Certificate issued: {certificate.id}")
        return certificate

    def get_certificate(self, certificate_id: int) -> Optional[Certificate]:
        return self.session.get(Certificate, certificate_id)
