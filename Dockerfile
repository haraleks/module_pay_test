FROM python:3.8.3-alpine
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN mkdir /module_pay
WORKDIR /module_pay
ADD requirements.txt /module_pay/
RUN apk add --no-cache libressl-dev musl-dev libffi-dev
RUN apk update \
    && apk add postgresql-dev gcc python3-dev
RUN apk upgrade --update-cache --available && \
    apk add openssl && \
    rm -rf /var/cache/apk/*
RUN apk --no-cache add build-base \
                       # dev dependencies
                       py3-pip \
                       # Pillow dependencies
                       jpeg-dev \
                       zlib-dev \
                       freetype-dev \
                       lcms2-dev \
                       openjpeg-dev \
                       tiff-dev \
                       tk-dev \
                       tcl-dev \
                       harfbuzz-dev \
                       fribidi-dev
# install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
ADD . /module_pay/