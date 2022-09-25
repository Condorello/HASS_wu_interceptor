ARG BUILD_FROM
FROM $BUILD_FROM

ENV LANG C.UTF-8

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# Install requirements for add-on
RUN \
    apk add --no-cache \
         python3 \
             py3-pip \
     \
     && pip3 install paho-mqtt

# Copy root filesystem

#COPY rootfs /

# Copy data for add-on
COPY run.sh /
COPY pws_server.py /
RUN chmod a+x /run.sh

CMD [ "/run.sh" ]
