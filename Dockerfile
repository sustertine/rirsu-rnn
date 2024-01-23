FROM python:3.11-slim
LABEL authors="Tine Šuster"

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -v -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
