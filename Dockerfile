FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY backend.py core.py interface.py ./
COPY prompts/ prompts/



EXPOSE 5000

CMD ["gunicorn", "backend:app", "--bind", "0.0.0.0:5000", "--workers", "3"]