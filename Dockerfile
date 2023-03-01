FROM python:3.7-alpine

COPY requirements.txt /rems_event_handler/
WORKDIR /rems_event_handler

RUN pip3 install -r requirements.txt

COPY . /rems_event_handler
EXPOSE 3009
CMD ["./rems_event_handler.py"]