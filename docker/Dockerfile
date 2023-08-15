ARG FROM_IMAGE=pytorch/torchserve:latest-gpu
FROM $FROM_IMAGE

USER root
RUN apt update
RUN apt-get install -y curl
RUN apt-get install -y nano
USER model-server

WORKDIR /home/model-server

# Install python dependencies
ADD docker/requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Include model files
COPY ../model_store /home/model-server/model-store

ENTRYPOINT ["/usr/local/bin/dockerd-entrypoint.sh"]
CMD ["serve"]