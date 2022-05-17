FROM python:latest

ADD . /home/app-server/

WORKDIR /home/app-server/

RUN apt-get update && apt-get install -y python3-opencv

RUN pip3 install opencv-python

RUN pip3 install --upgrade pip

RUN pip3 install -r requirements.txt

CMD exec gunicorn --bind 0.0.0.0:5000 --timeout=150 app:app -w 1

EXPOSE 5000