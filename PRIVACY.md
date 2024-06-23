# Privacy Statement

Hey, we are the lead developers of Modmail bot. This is a look into the data you collect, the data other parties collect, and what can be done about any of this data.  
> **Disclaimer**: None of us are lawyers. We are just trying to be more transparent.

This version of Modmail is a fork, and this privacy policy is a fork of the original Modmail privacy policy.
All telemetry and data collection has been removed from this fork.

**Plugins may collect additional data**. Please check with the plugin developer for more information.

### TL;DR

You collect some data to keep the bot functioning. External services also collect some data that is out of our control.

## Interpretation

- Modmail: This application that has been made open-source.
- Modmail Team: Lead developers, namely kyb3r, fourjr and taku.
- Bot: Your instance of the Modmail bot.
- Bot owner: The person managing the bot.
- Guild: A [server](https://discord.com/developers/docs/resources/guild#guild-resource), an isolated collection of users and channels, within Discord
- User: The end user, or server members, that interface with the bot.
- Database: A location where data is stored, hosted by the bot owner. The following types of database are currently supported: [MongoDB](#MongoDB).
- Logviewer: A webserver hosted by the bot owner.

## The Data You Collect

When using the bot, the bot can collect various bits of user data to ensure that the bot can run smoothly.    
This data is stored in a database instance that is hosted by the bot owner (more details below).

When a thread is created, the bot saves the following data:
- Timestamp
- Log Key
- Channel ID
- Guild ID
- Bot ID
- Recipient ID
- Recipient Username and Discriminator
- Recipient Avatar URL
- Whether the recipient is a moderator

When a message is sent in a thread, the bot saves the following data:
- Timestamp
- Message ID
- Message author ID
- Message author username and discriminator
- Message author avatar URL
- Whether the message author is a moderator
- Message content
- All attachment urls in the message

This data is essential to have live logs for the web logviewer to function.    
The Modmail team does not track any data by users.

### Opting out

There is no way for users or moderators to opt out from this data collection.

### Data deletion

Logs can be deleted using the `?logs delete <key>` command. This will remove all data from that specific log entry from the database permenantly.

## The Data Other Parties Collect

Plugins form a large part of the Modmail experience. Although we do not have any control over the data plugins collect, including plugins within our registry, all plugins are open-sourced by design. Some plugin devs may collect data beyond our control, and it is the bot owner's responsibility to check with the various plugin developers involved.

We recommend 4 external services to be used when setting up the Modmail bot.    
We have no control over the data external parties collect and it is up to the bot owner's choice as to which external service they choose to employ when using Modmail.    
If you wish to opt out of any of this data collection, please view their own privacy policies and data collection information. We will not provide support for such a procedure.

### Discord

- [Discord Privacy Policy](https://discord.com/privacy)

### MongoDB

- [MongoDB Privacy Policy](https://www.mongodb.com/legal/privacy-policy).

### Github

- [Github Privacy Statement](https://docs.github.com/en/free-pro-team@latest/github/site-policy/github-privacy-statement)

## Maximum Privacy Setup

For a maximum privacy setup, we recommend the following hosting procedure. We have included links to various help articles for each relevant step. We will not provide support for such a procedure.
- [Creating a local mongodb instance](https://zellwk.com/blog/local-mongodb/)
- [Hosting Modmail on your personal computer](https://docs.modmail.dev/)
- [Opt out of discord data collection](https://support.discord.com/hc/en-us/articles/360004109911-Data-Privacy-Controls)
- Do not use any plugins, setting `enable_plugins` to `no`.
