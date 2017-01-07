FROM python:2.7
RUN mkdir /api
WORKDIR /api
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 5001
ENTRYPOINT python api.py

