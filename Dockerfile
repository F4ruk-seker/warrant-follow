FROM cypress/browsers:latest

RUN apt-get install python3 -y

RUN echo $(python3 -m site --user-base)

COPY requirements.txt  .

ENV PATH /home/root/.local/bin:${PATH}

ENV BW_PATH ${cypress/browsers:latest}
ENV BW_PATHQ ${browsers:latest}

RUN  apt-get update && apt-get install -y python3-pip && pip install -r requirements.txt  

COPY . .

CMD python3 main.py