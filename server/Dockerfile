FROM python:3.8

WORKDIR /server/

ADD ./requirements.txt /server/requirements.txt
RUN pip install -r ./requirements.txt

ADD . /server/
CMD ["python", "server.py"]