FROM python:3.8-slim
# FROM postgres:14
RUN mkdir /app
WORKDIR /app
COPY app.py .
COPY models.py .
COPY requirements.txt .

RUN pip install --upgrade pip

EXPOSE 8080
RUN pip install -r requirements.txt

ENTRYPOINT ["python", "./app.py"]


