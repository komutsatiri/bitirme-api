FROM python:2.7
RUN mkdir /api
WORKDIR /api
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY api.py api.py

