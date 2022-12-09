FROM python:3.8
# set work directory
# copy project
WORKDIR /server/
# copy project
COPY . /server/
# install dependencies
RUN pip install -r ./requirements.txt
CMD ["python", "server.py"]