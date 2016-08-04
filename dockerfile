FROM cassandra
MAINTAINER luxu

USER root

#install flask
#RUN	apt-get -y install apt-utils
#RUN	apt-get -y upgrade
RUN 	apt-get update
RUN	apt-get -y install python-pip

RUN	apt-get -y install curl 

RUN	pip install --upgrade pip
RUN	pip install Flask
RUN	pip install watson-developer-cloud
RUN	pip install cassandra-driver

#build py
ADD	hello.py /home
ADD	h1.py /home
#RUN	chmod 777 /home/h1.py

#RUN	python /home/hello.py
WORKDIR /home
ENTRYPOINT ["python"]
CMD	   ["h1.py"]


