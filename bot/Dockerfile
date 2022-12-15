FROM python:3.8
# set work directory
WORKDIR /bot/
# copy project
ADD ./requirements.txt /bot/requirements.txt
RUN pip install -r ./requirements.txt

ADD . /bot/
CMD ["python", "app.py"]