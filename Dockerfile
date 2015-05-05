FROM docker.io/centos
MAINTAINER Manuel Sanchez <mannysanchez998@gmail.com>

LABEL Description="This image contains a minimal LAMP setup with sshd installed"

# Update packages
RUN yum update -y

# Install epel
RUN yum install -y epel-release

# Install ansible
RUN yum install -y ansible

# Copy ansible files
ADD playbooks /tmp/playbooks

# Run playbook
RUN ansible-playbook /tmp/playbooks/main.yml

# Remove all tmp files (includes playbooks)
RUN rm -rf /tmp/*
