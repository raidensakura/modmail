<div align="center">
  <img src="https://modmail-docs.netlify.app/logo-long.png" align="center"><br>
  <strong><i>Raiden's personal fork of Python Discord Modmail bot.</i></strong><br><br>

  <a href="#"><img src="https://img.shields.io/badge/Version-4.2.0-7d5edd?style=shield&logo=https://modmail-docs.netlify.app/favicon.png"></a>
  <img src="https://img.shields.io/badge/3.8_--_3.11-red?logo=python&logoColor=white&label=Python&labelColor=%233772a2&color=%23ffdd54">
  <a href="https://github.com/ambv/black"><img src="https://img.shields.io/badge/Code%20Style-Black-black?style=shield"></a>
  <a href="https://github.com/modmail-dev/modmail/blob/master/LICENSE"><img src="https://img.shields.io/badge/License-AGPL--3.0-e74c3c.svg?style=shield" alt="MIT License"></a>
  <a href="https://discord.gg/cnUpwrnpYb"><img src="https://img.shields.io/discord/616969119685935162.svg?label=Discord&logo=Discord&colorB=7289da&style=shield" alt="Support"></a>

<img src='https://github.com/raidensakura/modmail/assets/38610216/106e8fa3-6f8e-4b00-9968-f5c2f3108da0' align='center' width=500>
</div>

## Why hard fork?

Several fundamental issues for the official Modmail require fixes that are backward-incompatible, hence I decided to make this fork since it's unlikely my PR will be accepted. As this is a pretty niche use-case, most users should probably not use this. As a disclaimer, **I will not be responsible for any damage caused to your Modmail instance by using my fork.** This is made public simply for the spirit of open-source software.

This is mainly maintained by [@raidensakura](https://github.com/raidensakura) and [@khakers](https://github.com/khakers).

## Installation

This is a general installation guide for developers. Refer to the [documentation](https://modmail-docs.netlify.app) for user guide.

This guide assumes you have installed **git**, a **compatible Python version** and [**Poetry**](https://python-poetry.org/) installed.

1. Clone the repository
    ```console
    $ git clone https://github.com/raidensakura/modmail
    $ cd modmail
    ```
2. Create a Discord bot account, grant the necessary intents, and invite the bot.
3. Create a free MongoDB database.
4. Rename the file `.env.example` to `.env` and fill it with appropriate values
5. Install the Python dependencies and run the bot
    ```console
    $ poetry install --no-root
    $ poetry run python bot.py
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

Issues with this fork can be opened through [GitHub Issues](https://github.com/raidensakura/modmail/issues/new/choose).

Support for this forked version of Modmail can be requested through [Raiden's Discord server](https://dsc.gg/transience).
As I don't have a dedicated team to answer questions and provide help, response may not be as fast as official support.

## Contributing

Check out the [contributing guidelines](https://github.com/raidensakura/modmail/blob/stable/.github/CONTRIBUTING.md) before you get started.

The [develop](https://github.com/raidensakura/modmail/tree/develop) branch is where most of the features are tested before stable release.

This project has included pre-commit script that automatically run black and ruff linter on every commit.

1. Install development dependencies
    ```console
    $ poetry install --no-root --only dev
    ```
2. Install the pre-commit hook
    ```console
    $ poetry run pre-commit install
    ```
    
Alternatively, you can also lint the codebase manually

```console
$ poetry run black .
$ poetry run ruff .
```
