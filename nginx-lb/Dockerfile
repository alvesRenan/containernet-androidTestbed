FROM nginx:alpine

RUN apk add python3 py-pip iproute2 bridge-utils bash

RUN pip install python-nginx

COPY ./nginx.conf /etc/nginx/nginx.conf

COPY ./start.py /home/start.py

CMD ["nginx", "-g", "daemon off;"]