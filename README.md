<div align="center">
  <img src="https://modmail-docs.netlify.app/logo-long.png" align="center">
  <br>
  <strong><i>Fork of a feature-rich Modmail bot for Discord written in Python.</i></strong>
  <br>
  <br>

  <a href="#">
    <img src="https://img.shields.io/badge/Version-4.0.2-7d5edd?style=shield&logo=https://modmail-docs.netlify.app/favicon.png">
  </a>
  <a href="https://discord.gg/cnUpwrnpYb">
    <img src="https://img.shields.io/discord/1079074933008781362.svg?label=Discord&logo=Discord&colorB=7289da&style=shield" alt="Support">
  </a>
  <a href="https://ko-fi.com/raidensakura">
    <img src="https://img.shields.io/badge/kofi-donate-gold.svg?style=shield&logo=Ko-fi" alt="Ko-fi">
  </a>
  <a href="https://www.python.org/downloads/">
    <img src="https://img.shields.io/badge/Compatible%20With-Python%203.8%20|%203.9%20|%203.10%20|%203.11-blue.svg?style=shield&logo=Python" alt="Made with Python 3.8">
  </a>
  <a href="https://github.com/ambv/black">
    <img src="https://img.shields.io/badge/Code%20Style-Black-black?style=shield">
  </a>
  <a href="https://github.com/modmail-dev/modmail/blob/master/LICENSE">
    <img src="https://img.shields.io/badge/license-agpl-e74c3c.svg?style=shield" alt="MIT License">
  </a>

<img src='https://github.com/raidensakura/modmail/assets/38610216/106e8fa3-6f8e-4b00-9968-f5c2f3108da0' align='center' width=500>
</div>

## Features

* **Highly Customisable:**
  * Bot activity, prefix, category, log channel, etc.
  * Command permission system.
  * Interface elements (color, responses, reactions, etc.).
  * Snippets and *command aliases*.
  * Minimum duration for accounts to be created before allowed to contact Modmail (`account_age`).
  * Minimum length for members to be in the guild before allowed to contact Modmail (`guild_age`). 

* **Advanced Logging Functionality:**
  * When you close a thread, Modmail will generate a [log link](https://logs.modmail.dev/example) and post it to your log channel.
  * Native Discord dark-mode feel.
  * Markdown/formatting support.
  * Login via Discord to protect your logs (optional feature).
  * See past logs of a user with `?logs`.
  * Searchable by text queries using `?logs search`.

* **Robust implementation:**
  * Schedule tasks in human time, e.g. `?close in 2 hours silently`.
  * Editing and deleting messages are synced.
  * Support for the diverse range of message contents (multiple images, files).
  * Paginated commands interfaces via reactions.

This list is ever-growing thanks to active development and our exceptional contributors. See a full list of documented commands by using the `?help` command.

## Installation

This is a general installation guide. Refer to the [documentation](https://modmail-docs.netlify.app) for detailed user guide.

This guide assumes you have git, and a supported Python version installed and added to system PATH.

1. Clone the repository
    ```console
    $ git clone https://github.com/raidensakura/modmail
    $ cd modmail
    ```
2. Create a Discord bot account, grant the necessary intents, and invite the bot.
3. Create a free MongoDB database.
4. Rename the file `.env.example` to `.env` and fill it with appropriate values
5. Update pip, install pipenv, and install dependencies using pipenv
    ```console
    $ pip install -U pip
    $ pip install pipenv
    $ pipenv install
    ```
6. Start the bot
    ```console
    $ pipenv run bot
    ```
7. Load the logviewer plugin included with Modmail with `?plugin load @local/logviewer`

### Running the Docker Image

This guide assume you already have Docker or Docker Compose installed.

- Running with docker:
  ```console
  $ docker run --env-file=.env --name=modmail ghcr.io/raidensakura/modmail:stable
  ```
- Running with Docker Compose:
    ```console
    $ docker compose up -d
    ```
    
## Plugins

Modmail supports the use of third-party plugins to extend or add functionalities to the bot.
Plugins allow niche features as well as anything else outside of the scope of the core functionality of Modmail. 

You can find a list of third-party plugins using the `?plugins registry`  command on the bot or by reading through the official [REGISTRY.json](https://github.com/modmail-dev/modmail/blob/master/plugins/registry.json).

To develop your own, check out the [plugins documentation](https://github.com/modmail-dev/modmail/wiki/Plugins).

Plugins requests and support are available in the [Modmail Support Server](https://discord.gg/cnUpwrnpYb).

## Support & Issues

Issues with the bot can be opened through [GitHub Issues](https://github.com/raidensakura/modmail/issues/new/choose).

Support for this forked version of Modmail can be requested through [Raiden's Discord server](https://dsc.gg/transience).
As I don't have a dedicated team to answer questions and provide help, it will be be answered when I'm available.

## Contributing

Check out the [contributing guidelines](https://github.com/raidensakura/modmail/blob/stable/.github/CONTRIBUTING.md) before you get started.

The [develop](https://github.com/raidensakura/modmail/tree/develop) branch is where most of the features are tested before stable release.

This project has included pre-commit script that automatically runs black and ruff linter on every commit.

1. Install development dependencies inside pipenv
    ```console
    $ pipenv install --dev
    ```
2. Install the pre-commit hook
    ```console
    $ pre-commit install
    ```
    
Alternatively, you can also lint the codebase manually

```console
$ black .
$ ruff .
```
