FROM python:3.8
# set work directory
# copy project
WORKDIR /server/
# copy project

ADD ./requirements.txt /server/requirements.txt
RUN pip install -r ./requirements.txt

ADD . /server/
CMD ["python", "server.py"]