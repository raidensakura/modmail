FROM python:3.11-alpine as base

RUN apk update && apk add git \
	# cairosvg dependencies
	cairo-dev cairo cairo-tools \
	# pillow dependencies
	jpeg-dev zlib-dev

FROM base as python-deps

RUN apk add --virtual build-deps build-base gcc libffi-dev
COPY requirements.txt /
RUN pip install --prefix=/inst -U -r /requirements.txt

FROM base as runtime

ENV USING_DOCKER yes
COPY --from=python-deps /inst /usr/local

COPY . /modmail
WORKDIR /modmail

CMD ["python", "bot.py"]

RUN adduser --disabled-password --gecos '' app && \
    chown -R app /modmail
USER app