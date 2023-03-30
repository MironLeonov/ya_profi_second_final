FROM python:3.8
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN apt-get update
RUN apt-get install -y libpq-dev
RUN pip3 install -r requirements.txt
COPY . .
EXPOSE 8080
ENTRYPOINT uvicorn main:app --port 8080 --host 0.0.0.0