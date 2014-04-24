FROM ubuntu:precise

RUN apt-get update && apt-get install python-pip python-dev msgpack-python imagemagick -y
RUN pip install cocaine PIL

ADD worker.py /filterapp/
ADD converter.py /filterapp/
ADD frames /filterapp/

