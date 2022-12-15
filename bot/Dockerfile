FROM python:3.8

WORKDIR /bot/

ADD ./requirements.txt /bot/requirements.txt
RUN pip install -r ./requirements.txt

ADD . /bot/
CMD ["python", "app.py"]