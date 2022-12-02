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
RUN pip install -r ./requirements.txt
# RUN chmod +x install.sh
# run app
RUN git lfs clone --progress https://huggingface.co/KiRiLLBEl/MovieDescriptionGen
CMD ["python", "server.py"]
# ENTRYPOINT [ "/server/install.sh" ]