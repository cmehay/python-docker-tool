# Docker demo, this doesn't have any purpose but for testing

FROM python:3

ADD . /opt/docker-tools/

RUN pip3 install pytest

WORKDIR /opt/docker-tools/

CMD ["py.test", "."]
