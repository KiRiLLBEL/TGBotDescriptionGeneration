FROM python:3.8
# set work directory
# copy project
WORKDIR /server/
# copy project
COPY . /server/
# install dependencies
RUN apt-get update
RUN apt-get install git
RUN apt-get install git-lfs
RUN git lfs clone https://huggingface.co/KiRiLLBEl/MovieDescriptionGen
RUN pip install -r ./requirements.txt
# run app
CMD ["python", "consumer.py"]