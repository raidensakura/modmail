<div align="center">
  <img src="https://modmail-docs.netlify.app/logo-long.png" align="center"><br>
  <strong><i>A Modmail fork with a focus on improvements and bug fixes.</i></strong><br><br>

  <img alt="Dynamic TOML Badge" src="https://img.shields.io/badge/dynamic/toml?url=https%3A%2F%2Fraw.githubusercontent.com%2Fraidensakura%2Fmodmail%2Fstable%2Fpyproject.toml&query=tool.poetry.version&style=flat&label=Version&color=7d5edd">
  <img alt="Dynamic TOML Badge" src="https://img.shields.io/badge/dynamic/toml?url=https%3A%2F%2Fraw.githubusercontent.com%2Fraidensakura%2Fmodmail%2Fstable%2Fpyproject.toml&query=tool.poetry.dependencies.python&style=flat&logo=python&logoColor=white&label=Python&labelColor=%233772a2&color=%23ffdd54">
  <img alt="Docker Pulls" src="https://img.shields.io/docker/pulls/raidensakura/modmail?label=Docker%20Pulls&link=https%3A%2F%2Fgithub.com%2Fraidensakura%2Fmodmail%2Fpkgs%2Fcontainer%2Fmodmail">
  <a href="https://github.com/ambv/black"><img src="https://img.shields.io/badge/Code%20Style-Black-black?style=shield"></a>
  <img alt="GitHub License" src="https://img.shields.io/github/license/raidensakura/modmail?link=https%3A%2F%2Fgithub.com%2Fraidensakura%2Fmodmail%2Fblob%2Fstable%2FLICENSE">
  <a href="https://discord.gg/cnUpwrnpYb"><img src="https://img.shields.io/discord/616969119685935162.svg?label=Discord&logo=Discord&colorB=7289da&style=shield" alt="Support"></a>

<img src='https://github.com/raidensakura/modmail/assets/38610216/106e8fa3-6f8e-4b00-9968-f5c2f3108da0' align='center' width=500>
</div>

## Why hard fork?

Modmail has quite a few significant problems with its feature implementations, ranging from improper Discord sticker support down to suboptimal user blocking feature. Inevitably, fixing these fundametal issues required backward-incompatible fixes and since Modmail is rather slow on updates, I decided to turn this into a public hard fork for other user's benefits and for the spirit of FOSS.

**Important disclaimer:** This fork is neither supported nor endorsed by the Official Modmail team. __Do not ask__ the official support team if you have issues on this forked version. Since most of the modifications implemented are backward-incompatible, I will not be responsible for the damage caused to your Modmail instance by using this fork.

## Installation

This is a general installation guide for developers. Refer to the [documentation](https://modmail-docs.netlify.app) for user guide.

This guide assumes you have installed **git**, a **compatible Python version** and [**Poetry**](https://python-poetry.org/) / [**PDM**](https://pdm-project.org/) installed.

1. Clone the repository
    ```console
    $ git clone https://github.com/raidensakura/modmail
    $ cd modmail
    ```
2. Create a Discord bot account, grant the necessary intents, and invite the bot.
3. Create a MongoDB database and a user for the bot to connect to.
4. Rename the file `.env.example` to `.env` and fill it with appropriate values.
5. Install project dependencies and run the bot.
	- Using Poetry:  

		```console
		$ poetry install --no-root
		$ poetry run python bot.py
		```
	- Using PDM:

		```console
		$ pdm install
		$ pdm run python bot.py
		```
7. [Optional] Load the logviewer plugin with `[p]plugin load raidensakura/modmail-plugins/logviewer@main`

## Running the Docker Image

This guide assume you already have Docker or Docker Compose installed.

- Running with docker:
  ```console
  $ docker run --env-file=.env --name=modmail ghcr.io/raidensakura/modmail:stable
  ```
- Running with Docker Compose:
    ```console
    $ docker compose up -d
    ```

## Support & Issues

This is mainly maintained by [@raidensakura](https://github.com/raidensakura), issues and support questions can be raised via [Discord Server](https://dsc.gg/transience) or [GitHub Issues](https://github.com/raidensakura/modmail/issues/new/choose). 

## Contributing

Check out the [contributing guidelines](https://github.com/raidensakura/modmail/blob/stable/.github/CONTRIBUTING.md) before you get started.

The [develop](https://github.com/raidensakura/modmail/tree/develop) branch is where most of the features are tested before stable release.

This project has included pre-commit script that automatically run black and ruff linter on every commit.

1. Install development dependencies.
    ```console
    $ poetry install --no-root --only dev
    ```
2. Install the pre-commit hook.
    ```console
    $ poetry run pre-commit install
    ```
    
Alternatively, you can also lint the codebase manually

```console
$ poetry run black .
$ poetry run ruff .
```
