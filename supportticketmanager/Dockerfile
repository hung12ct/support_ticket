FROM python:3.7.5-buster

# set up the psycopg2
RUN apt-get update && apt-get install -y libpq-dev gcc postgresql-client
RUN pip install psycopg2==2.8.4
RUN apt-get autoremove -y gcc

# set work directory
WORKDIR /opt/supportticketmanager

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /opt/supportticketmanager/requirements.txt
RUN chmod +x /opt/supportticketmanager/requirements.txt
RUN pip install -r requirements.txt

# copy project
COPY . /opt/supportticketmanager/

RUN chmod +x /opt/supportticketmanager/start.sh
ENTRYPOINT [ "/opt/supportticketmanager/start.sh" ]