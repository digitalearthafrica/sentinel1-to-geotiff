FROM ubuntu:18.10

RUN apt-get update && apt-get install -y python3-pip gdal-bin python3-gdal
RUN apt-get install wget

ADD requirements.txt /tmp/
RUN pip3 install -r /tmp/requirements.txt

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

ADD esa-snap_sentinel_unix_7_0.sh  /tmp/

CMD /tmp/esa-snap_sentinel_unix_7_0.sh


RUN mkdir -p /opt/s1/

WORKDIR /opt/s1/
