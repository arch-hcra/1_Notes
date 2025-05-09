FROM python:3.9-slim

WORKDIR /file_service

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5001

CMD ["python", "file_service.py"]
