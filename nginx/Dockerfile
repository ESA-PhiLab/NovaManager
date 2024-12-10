FROM nginx:alpine

RUN apk update && \
    apk add --no-cache openssl && \
    rm /etc/nginx/conf.d/default.conf && \
    mkdir -p /etc/nginx/certs && \
    openssl req -x509 -nodes -days 3650 -newkey rsa:2048 -subj "/C=IT/ST=LAZIO/O=ESA/CN=" -keyout /etc/nginx/certs/nginx.key -out /etc/nginx/certs/nginx.crt;

COPY nginx.conf /etc/nginx/conf.d   
