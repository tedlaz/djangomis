FROM python:3.7-slim

WORKDIR /misthodosia

COPY . ./

RUN pip install -r requirements.txt

EXPOSE 8000

ENTRYPOINT ["gunicorn", "--bind", "0.0.0.0:8000", "djangomis.wsgi"]
