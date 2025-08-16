# templates-celery

PDF templates with Celery.

To install the Conda environment:

```
conda env create -f environment.yml
```

To install dependencies:

```
poetry install
```

To run FastAPI in dev mode:

```
PYTHONPATH=. fastapi dev templates/fastapi/controller.py
```

To access the Swagger endpoints, go to http://localhost:8000/docs

To run the Celery server:

```
celery -A templates.celery.tasks worker --loglevel=INFO
```