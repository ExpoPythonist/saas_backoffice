FROM python:3.7.2

ENV PYTHONUNBUFFERED 1
WORKDIR /code

# Run this first so the first image layer is cached
ADD requirements.txt /code/
RUN pip install -r requirements.txt

ADD ./ /code/

RUN echo "test"
