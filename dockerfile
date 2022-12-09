FROM ubuntu:latest
COPY ele_bot.py .
COPY requirements.txt .
RUN apt-get update && apt-get -y install python3-pip && pip install --upgrade pip==22.3.1 && apt-get install -y iputils-ping
RUN apt-get -y install micro
RUN pip install -r requirements.txt 
CMD python3 ele_bot.py $ENDP