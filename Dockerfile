FROM python:3.9-buster

WORKDIR /app

#Recommended by Docker itself
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY . .

RUN pip install --upgrade pip &&  \
    apt-get update &&\
    apt-get install -y --no-install-recommends gcc libc-dev python3-dev netcat &&\
    pip install --no-cache-dir -r requirements.txt &&\
    mkdir /app/staticfiles &&\
    python manage.py collectstatic --no-input --clear &&\
    rm -rf /app/static_dev/* &&\
    useradd user &&\
    chown -R user:user /app &&\
    chmod -R 755 /app

USER user

ENTRYPOINT ["/app/scripts/docker-entrypoint.sh"]