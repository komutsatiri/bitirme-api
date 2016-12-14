FROM python:2.7
ADD . /api
WORKDIR /api
RUN pip install -r requirements.txt
EXPOSE 5001
CMD python api.py
