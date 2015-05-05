FROM docker.io/centos
MAINTAINER Manuel Sanchez <mannysanchez998@gmail.com>

LABEL Description="This image contains a minimal LAMP setup with sshd installed"
# Install LAMP
RUN yum install -y httpd mariadb mariadb-server php php-mysql 
# Install sshd
RUN yum install -y openssh-server
# Create ssh keys
RUN /usr/bin/ssh-keygen -A
# Install python setuptools
RUN yum install -y python-setuptools
# Install supervisor
RUN easy_install supervisor
# Copy supervisord.conf
COPY supervisord.conf /etc/supervisord.conf
