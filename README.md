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
    <img src="https://img.shields.io/badge/Compatible%20With-Python%203.8%20|%203.9%20|%203.10-blue.svg?style=shield&logo=Python" alt="Made with Python 3.8">
  </a>
  <a href="https://github.com/ambv/black">
    <img src="https://img.shields.io/badge/Code%20Style-Black-black?style=shield">
  </a>
  <a href="https://github.com/modmail-dev/modmail/blob/master/LICENSE">
    <img src="https://img.shields.io/badge/license-agpl-e74c3c.svg?style=shield" alt="MIT License">
  </a>

<img src='https://github.com/raidensakura/modmail/assets/38610216/106e8fa3-6f8e-4b00-9968-f5c2f3108da0' align='center' width=500>
</div>


## What is Modmail?

Modmail is similar to Reddit's Modmail, both in functionality and purpose. It serves as a shared inbox for server staff to communicate with their users in a seamless way.

This bot is free for everyone and always will be. If you like this project and would like to show your appreciation, you can support the original developers on their **[Patreon](https://www.patreon.com/kyber)**, cool benefits included! 

## How does it work?

When a member sends a direct message to the bot, Modmail will create a channel or "thread" into a designated category. All further DM messages will automatically relay to that channel; any available staff can respond within the channel.

Logviewer will save the threads so you can view previous threads through their corresponding log link.

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

Q: Where can I find the Modmail bot invite link?

A: Unfortunately, due to how this bot functions, it cannot be invited. The lack of an invite link is to ensure an individuality to your server and grant you full control over your bot and data. Nonetheless, you can quickly obtain a free copy of Modmail for your server by following one of the methods listed below (roughly takes 15 minutes of your time).

There are a few options for hosting your very own dedicated Modmail bot.

1. Patreon hosting
2. Local hosting (VPS, Dedicated Server, RPi, your computer, etc.)
3. PaaS (we provide a guide for Heroku)

### Patreon Hosting

If you don't want the trouble of renting and configuring your server to host Modmail, the original developers offer hosting and maintenance of your own, private Modmail bot (including a Logviewer) through [**Patreon**](https://patreon.com/kyber). Join our [Modmail Discord Server](https://discord.gg/cnUpwrnpYb) for more info! 

### Local hosting (General Guide)

Modmail can be hosted on any modern hardware, including your PC. For stability and reliability, we suggest purchasing a cloud server (VPS) for under $10/mo. If you need recommendations on choosing a VPS, join the [Discord server](https://discord.gg/cnUpwrnpYb), and we'll send you a list of non-affiliated hosting providers. Alternatively, we can host Modmail for you when you're subscribed to the [Patreon](https://patreon.com/kyber).

This guide assumes you've downloaded [`Python 3.10`](https://www.python.org/downloads/release/python-376/) and added python and pip to PATH.

1. Clone this repo
    ```console
    $ git clone https://github.com/modmail-dev/modmail
    $ cd modmail
    ```
2. Create a Discord bot account, grant the necessary intents, and invite the bot ([guide](https://github.com/modmail-dev/modmail/wiki/Installation#2-discord-bot-account))
3. Create a free MongoDB database ([guide](https://github.com/modmail-dev/modmail/wiki/Installation-(cont.)#3-create-a-database), follow it carefully!)
4. Rename the file `.env.example` to `.env` and fill it with appropriate values
   - If you can't find `.env.example` because it's hidden, create a new text file named `.env`, then copy the contents of [this file](https://raw.githubusercontent.com/modmail-dev/modmail/master/.env.example) and replace the placeholders with their values
   - If you're on Windows and cannot save the file as `.env`, save it as `.env.` instead (this only applies to Windows!)
   - If you do not have a Logviewer yet, leave the `LOG_URL` field as-is
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
7. Set up the Logviewer, see the [Logviewer installation guide](https://github.com/modmail-dev/logviewer)

### Local Hosting (Docker)

We provide support for Docker to simplify the deployment of Modmail and Logviewer. 
We assume you already have Docker and Docker Compose Plugin installed, if not, see [here](https://docs.docker.com/get-docker/).

1. Create a Discord bot account, grant the necessary intents, and invite the bot ([guide](https://github.com/modmail-dev/modmail/wiki/Installation#2-discord-bot-account))
2. Create a file named `.env`, then copy the contents of [this file](https://raw.githubusercontent.com/modmail-dev/modmail/master/.env.example) and replace the placeholders with their values
3. Create a file named `docker-compose.yml`, then copy the contents of [this file](https://raw.githubusercontent.com/modmail-dev/modmail/master/docker-compose.yml), do not change anything!
4. Start the bot
    ```console
    $ docker compose up -d
    ```
   - For older Docker versions, you may need to run `docker-compose up -d` instead
5. View the status of your bot, using `docker ps` and `docker logs [container-id]`

Docker images are hosted on [GitHub Container Registry](ghcr.io), you can build your own image if you wish:
```console
$ docker build --tag=modmail:stable .
```

Then simply remove `ghcr.io/modmail-dev/` from the `docker-compose.yml` file.

### Local Hosting (OS-Specific)

Refer to our [documentation](https://modmail-docs.netlify.app) for more info.

### Platform as a Service (PaaS)

You can host this bot on various PaaS such as Heroku, Railway, and others.

Installation via Heroku is possible with your web browser alone. 
The [**installation guide**](https://github.com/modmail-dev/modmail/wiki/Installation) (which includes a video tutorial!) will guide you through the entire installation process. If you run into any problems, join the [Modmail Discord Server](https://discord.gg/cnUpwrnpYb) for help and support.

When using Heroku, you can configure automatic updates:
 - Login to [GitHub](https://github.com/) and verify your account.
 - [Fork the repo](https://github.com/modmail-dev/modmail/fork).
 - Install the [Pull app](https://github.com/apps/pull) for your fork. 
 - Then go to the Deploy tab in your [Heroku account](https://dashboard.heroku.com/apps) of your bot app, select GitHub and connect your fork (usually by typing "Modmail"). 
 - Turn on auto-deploy for the `stable` branch.

## Sponsors

Special thanks to the sponsors for supporting the project.

SirReddit:
<br>
<a href='https://www.youtube.com/channel/UCgSmBJD9imASmJRleycTCwQ/featured'>
  <img height=100 src='https://i.imgur.com/WyzaPKY.png' style='margin:5px'>
</a>
<br>
<br>
Prime Servers Inc:
<br>
<a href='https://primeserversinc.com/'>
  <img height=100 src='https://i.imgur.com/sVcwtt8.png' style='margin:5px'>
</a>
<br>
<br>
Real Madrid:
<br>
<a href='https://discord.gg/realmadrid'>
  <img height=100 src='https://i.imgur.com/9Rat2Qb.png' style='margin:5px'>
</a>
<br>
<br>
Advertise Your Server:
<br>
<a href='https://discord.gg/zP8KcF4VQz'>
  <img height=100 src='https://user-images.githubusercontent.com/45324516/140673115-dd3e873c-36b6-4383-9eb4-db42e1986ab3.png' style='margin:5px'>
</a>
<br>
<br>
Discord Advice Center:
<br>
<a href='https://discord.gg/zmwZy5fd9v'>
  <img height=100 src='https://i.imgur.com/1hrjcHd.png' style='margin:5px'>
</a>


Become a sponsor on [Patreon](https://patreon.com/kyber).

## Plugins

Modmail supports the use of third-party plugins to extend or add functionalities to the bot.
Plugins allow niche features as well as anything else outside of the scope of the core functionality of Modmail. 

You can find a list of third-party plugins using the `?plugins registry`  command or visit the [Unofficial List of Plugins](https://github.com/modmail-dev/modmail/wiki/Unofficial-List-of-Plugins) for a list of plugins contributed by the community.

To develop your own, check out the [plugins documentation](https://github.com/modmail-dev/modmail/wiki/Plugins).

Plugins requests and support are available in the [Modmail Support Server](https://discord.gg/cnUpwrnpYb).

## Contributing

Contributions to Modmail are always welcome, whether it be improvements to the documentation or new functionality, please feel free to make the change. Check out the [contributing guidelines](https://github.com/raidensakura/modmail/blob/stable/.github/CONTRIBUTING.md) before you get started.

If you like this project and would like to show your appreciation, support us on **[Patreon](https://www.patreon.com/kyber)**!

## Beta Testing

The [develop](https://github.com/raidensakura/modmail/tree/develop) branch is where most of the features are tested before stable release. Be warned that there could be bugs in various commands so keep it away from any large servers you manage.

If you wish to test the new features and play around with them, feel free to join the [Public Test Server](https://discord.gg/v5hTjKC). Bugs can be raised within that server or in our Github issues (state that you are using the development branch though).
