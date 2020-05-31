<p align="center">
<img src="https://raw.githubusercontent.com/ruqqus/ruqqus/master/ruqqus/assets/images/logo/ruqqus_text_logo.png" width="250"/>
</p>

<hr>

# Ruqqus

Ruqqus is an open-source platform for online communities, free of censorship and moderator abuse by design.

![Build status](https://travis-ci.com/ruqqus/ruqqus.svg?branch=master) ![Snyk Vulnerabilities for GitHub Repo](https://img.shields.io/snyk/vulnerabilities/github/ruqqus/ruqqus) [![Website](https://img.shields.io/website/https/www.ruqqus.com?down_color=red&down_message=down&up_message=up)](https://www.ruqqus.com) ![GitHub language count](https://img.shields.io/github/languages/count/ruqqus/ruqqus) ![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/ruqqus/ruqqus) [![](https://img.shields.io/discord/599258778520518676)](https://discord.gg/U57jqnn)

<p align="center">
<img src="https://raw.githubusercontent.com/ruqqus/ruqqus/master/ruqqus/assets/images/preview-images/ruqqus_demo.png" width="720"/>
</p>

## Features

- Moderator power limited by design
- No ads
- US-based servers
- Mobile friendly
- Dark mode

## Why Ruqqus?

A moderator has the power to "kick" a user-submitted post from their community (guild) but never delete it off the platform entirely. Kicked posts end up in a catch-all guild called [+general](https://ruqqus.com/+general). Content that violates the [site-wide policy](https://ruqqus.com/help/terms) is removed by the core team.

Moderators, called guild masters, can only moderate a maximum of 10 guilds.

We do not serve ads. Put simply, advertisements lead to censorship. Ruqqus is funded out-of-pocket by the core team and through donations from users.

Ruqqus is responsive and mobile browser-friendly.

## Getting started

An account is not required to browse Ruqqus but we recommend creating one.

**1. Create an account**

[Sign up](https://ruqqus.com/signup?ref=ruqqus) in seconds, no email required. With a Ruqqus account, you can vote and comment on posts as well as join guilds.

**2. Join some guilds**

After signing up, we recommend you join some guilds. Your home feed will be populated by content from guilds you've joined.

**3. Create a post**

On Ruqqus, you can share links or text posts.

## Contributing

Pull requests are welcome! For major changes, please open an issue to discuss what you would like to change.

## Dev Setup

Docker is the easiest way to start developing on ruqqus.  Instructions were written with Linux in mind.
- edit your hosts file (`/etc/hosts`), add `dev.localhost` as a proxy for `127.0.0.1`, there should be a line that looks like: `127.0.0.1 localhost dev.localhost`
- run `docker-compose up` in the project root
- `sudo apt install postgresql-client`
- `psql -U unicorn_user -d ruqqus < schema.txt`, enter the password `magical_password`
- install 
- you should be able to see ruqqus at `http://dev.localhost:8000` in your browser.  There will be some errors.  This is due to ruqqus expecting a stickied post at all times, to fix this:
  - sign up for a user on your local instance
  - go to `http://localhost:5050`(pgAdmin) and connect to the db with the credentials in `docker-compose.yml`.
  - set the user's admin level to 100 in pgAdmin
  - go back to your local instance of ruqqus in your browser, create a guild, create a post
  - go back to pgAdmin and find your post, and sticky it.
- ruqqus should be more or less working now at `http://dev.localhost:8000`

- known issue:  some changes (like those to .html files) will not be picked up automatically, you have to change a .py file for changes to be picked up.  When in doubt, `docker-compose build && docker-compose up`.

## Sponsors

As an open-source project, we are supported by the community. If you would like to support the development of Ruqqus, please consider [making a donation](https://ruqqus.com/help/donate) :)

## Stay in touch

- [Twitter](https://twitter.com/ruqqus)
- [Discord](https://ruqqus.com/discord)
- [Twitch.tv](https://twitch.tv/captainmeta4)

## License
[MPL-2.0](https://github.com/ruqqus/ruqqus/blob/master/LICENSE)
