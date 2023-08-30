FROM ubuntu:latest
LABEL authors="seker"

ENV FIREFOX_PATH /usr/bin/firefox

RUN apt-get install -y firefox && apt-get clean

ENTRYPOINT ["top", "-b"]

CMD ["python", "main.py"]