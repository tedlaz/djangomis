FROM python:3.7-slim

copy requirements.txt /tmp/

RUN pip install -r /tmp/requirements.txt && \
    mkdir misthodosia

COPY . /misthodosia

RUN chmod +x /misthodosia/start.sh

WORKDIR /misthodosia

EXPOSE 8000

CMD ["/misthodosia/start.sh"]
