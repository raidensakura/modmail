FROM python:3.10-alpine as base

RUN apk update && apk add git cairo-dev cairo cairo-tools \
	# pillow dependencies
    jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev

FROM base AS python-deps

RUN apk add --virtual build-dependencies build-base gcc libffi-dev

COPY Pipfile Pipfile.lock /
RUN pip install pipenv && PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy

FROM base AS runtime

COPY --from=python-deps /.venv /.venv
ENV PATH="/.venv/bin:$PATH"

ENV USING_DOCKER yes
COPY . /modmail
WORKDIR /modmail

CMD ["python", "-m", "bot"]

RUN adduser --disabled-password --gecos '' app && \
    chown -R app /modmail && chown -R app /.venv
USER app
