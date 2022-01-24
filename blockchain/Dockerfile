FROM ubuntu:latest

RUN apt-get -y install update
RUN apt-get -y install upgrade
RUN apt-get -y install python3 python3-pip

ADD . .

CMD pip install --upgrade ecdsa numba
CMD python3 boot.py