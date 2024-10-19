FROM ubuntu: Latest

RUN apt-get update && apt-ger install -y \
      python3.10 \
      python3-pip \
      git

RUN pip3 install PyYAML

COPY feed.py /usr/bin/feed.py

COPY entrypoint.sh /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]