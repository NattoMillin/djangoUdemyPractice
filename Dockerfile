FROM python:3.8-slim
EXPOSE 8000
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

ARG UID=20000
ARG GID=20000
ARG PASSWORD="password"

RUN apt-get update
RUN apt-get install -y \
    sudo \
    git 

RUN groupadd -g $GID dev \
    && useradd -m -u $UID -g $GID dev && \
    echo dev:$PASSWORD | chpasswd && \
    echo "dev  ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers
#ユーザーを追加。

RUN mkdir /app
RUN chown -R dev /app
USER dev

WORKDIR /app

COPY django /app/

RUN python -m pip install -r requirements.txt

