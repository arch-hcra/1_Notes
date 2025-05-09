FROM python:3.9-slim

WORKDIR /display_service

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5003

CMD ["python", "display_service.py"]
