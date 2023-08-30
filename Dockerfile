FROM ubuntu:latest
LABEL authors="seker"

RUN apt-get install -y firefox && apt-get clean

CMD ["python", "main.py"]