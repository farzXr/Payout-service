FROM willhallonline/ansible:2.17-ubuntu-22.04

RUN apt update && \
    apt install -y sshpass dos2unix jq && \
    apt install curl -y && \
    pip install hvac