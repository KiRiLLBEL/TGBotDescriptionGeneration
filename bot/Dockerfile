FROM python:3.8
# set work directory
WORKDIR /bot/
# copy project
COPY . /bot/
# install dependencies
RUN pip install -r ./requirements.txt
# run app
CMD ["python", "bot.py"]