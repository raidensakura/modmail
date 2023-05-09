FROM python:3.10-alpine as base

RUN apk add wget git cairo-dev cairo cairo-tools \
	# pillow dependencies
    jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev

FROM base AS python-deps

# Install pipenv and compilation dependencies
RUN apk update && apk add --virtual build-dependencies build-base gcc libffi-dev
RUN pip install pipenv

# Install python dependencies in /.venv
COPY Pipfile Pipfile.lock /
RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy

FROM base AS runtime

# Copy virtual env from python-deps stage
COPY --from=python-deps /.venv /.venv
ENV PATH="/.venv/bin:$PATH"

# Create and switch to a new user
RUN adduser -D modmail
WORKDIR /home/modmail
USER modmail

# Install application into container
ENV USING_DOCKER yes
COPY . .

# Run the application
CMD ["python", "-m", "bot"]
