FROM ubuntu:latest
LABEL authors="seker"

ENV FIREFOX_PATH /usr/bin/firefox

ENTRYPOINT ["top", "-b"]

CMD ["python", "main.py"]