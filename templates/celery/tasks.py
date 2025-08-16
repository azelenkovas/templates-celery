from celery import Celery
from templates.services.certificate_service import CertificateService
from templates.models.template import Template
from templates.models.certrificate import CertificateRequest, Certificate
from templates.db.postgresql import engine, create_db_and_tables
from sqlmodel import Session
import logging

celery_app = Celery('templates', broker='redis://localhost:6379/0')

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# create_db_and_tables()

@celery_app.task
def issue_certificate(certificate_id: int):
    certificate_service = CertificateService(session=Session(engine))    
    certificate_service.issue_certificate(certificate_id)
    
   