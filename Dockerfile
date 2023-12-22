FROM python:3.11-alpine as base

RUN apk update && apk add git \
	# pillow dependencies
	jpeg-dev zlib-dev && \
	adduser -D -h /home/modmail -g 'Modmail' modmail

ENV PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /home/modmail

FROM base as poetry

RUN apk add build-base && \
	pip install -U poetry
COPY --chown=modmail:modmail poetry.lock pyproject.toml /home/modmail/
RUN python -m poetry export -o requirements.txt

FROM base as deps

USER modmail

COPY --from=poetry /home/modmail/requirements.txt /home/modmail/

RUN pip install -r requirements.txt --user

FROM deps as runtime

ENV PATH=/home/modmail/.local/bin:$PATH
COPY --chown=modmail:modmail . .

CMD ["python", "bot.py"]
