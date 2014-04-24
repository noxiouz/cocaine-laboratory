FROM ubuntu:precise

RUN apt-get update && apt-get install python-pip python-dev msgpack-python -y
RUN pip install cocaine flask

ADD worker.py /usr/bin/cocagram/
ADD app.py /usr/bin/cocagram/
ADD ui /usr/bin/cocagram/ui
ADD static /usr/bin/cocagram/static
ADD templates /usr/bin/cocagram/templates
