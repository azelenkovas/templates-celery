from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query, UploadFile, Form
from sqlmodel import Field, Session, SQLModel, create_engine, select
from templates.db.sqlite import create_db_and_tables, SessionDep
from templates.models.template import Template
from templates.services.template_service import InvalidTemplateException, TemplateService
import logging


app = FastAPI()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.on_event("startup")
def on_startup():
    logger.info("Creating database and tables...")    
    create_db_and_tables()
    logger.info("Database and tables created successfully.")
    
@app.post("/templates/")
def create_template(file: UploadFile, description: Annotated[str, Form()], session: SessionDep) -> Template:
    try:
        template = Template(name=file.filename, description=description)
        template.pdf_file = file.file.read()
    except AttributeError:
        raise HTTPException(status_code=400, detail="Invalid PDF file format")
    try:
        return TemplateService(session).create_template(template)
    except InvalidTemplateException as e:
        raise HTTPException(status_code=400, detail=str(e))    
    
@app.get("/templates/")
def read_templates(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[Template]:
    return TemplateService(session).get_templates(offset=offset, limit=limit)

@app.get("/templates/{template_id}")
def read_template(template_id: int, session: SessionDep) -> Template:
    template = TemplateService(session).get_template(template_id)
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    return template

@app.put("/templates/{template_id}")
def update_template(template_id: int, file: UploadFile, description: Annotated[str, Form()], session: SessionDep) -> Template:
    try:
        template = Template(id=template_id, name=file.filename, description=description)
        template.pdf_file = file.file.read()
    except AttributeError:
        raise HTTPException(status_code=400, detail="Invalid PDF file format")
    updated_template = TemplateService(session).update_template(template_id, template)
    if not updated_template:
        raise HTTPException(status_code=404, detail="Template not found")
    return updated_template

@app.delete("/templates/{template_id}")
def delete_template(template_id: int, session: SessionDep):
    deleted_template = TemplateService(session).delete_template(template_id)
    if not deleted_template:
        raise HTTPException(status_code=404, detail="Template not found")
    return {"ok": True}
