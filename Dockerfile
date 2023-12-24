FROM python:3.11-alpine as base

RUN apk update && apk add git \
	# pillow dependencies
	jpeg-dev zlib-dev && \
    pip install --upgrade pip && \
	adduser -D -h /home/modmail -g 'Modmail' modmail

WORKDIR /home/modmail

FROM base as builder

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

RUN apk add build-base libffi-dev && \
	pip install -U poetry

COPY --chown=modmail:modmail poetry.lock pyproject.toml /home/modmail/

RUN --mount=type=cache,target=$POETRY_CACHE_DIR poetry install --without dev --no-root

FROM base as runtime

ENV VIRTUAL_ENV=/home/modmail/.venv \
    PATH="/home/modmail/.venv/bin:$PATH" \
    USING_DOCKER=yes

COPY --from=builder --chown=modmail:modmail ${VIRTUAL_ENV} ${VIRTUAL_ENV}

COPY --chown=modmail:modmail . .

USER modmail

CMD ["python", "bot.py"]
