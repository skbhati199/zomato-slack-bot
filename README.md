# Zomato bot for slack

A simple slackbot. It uses _Zomato_ api to search for restaurants to get their daily menu.
If you find the code useful and make some changes to it please consider creating a pull-request *:)*

*WARNING - few hours of work*.
Unfortunately _Zomato_ does not seem to have an API for daily menus.
I used the `pyquery` library to parse the menu from their pages.
Any slight change of their web can break this code.

## Goals

The current hardcoded questions are dumb.
I would like to use [quepy](https://github.com/machinalis/quepy) to parse messages and translate them into _Zomato api_ queries.

## How to use it

You simply register a new bot to your Slack account and ask him/her to give you lunch menu of yout favourite restaurant.

### Dependencies
The code is base on `python3`. All the necesseary dependencies are available from pip.
 * `dateparser`
 * `pyquery`
 * `slackbot`
 * `requests`
 
You can instal the dependencies siply by executing `pip3 install -r requirements.pip`.

### Settings
Copy the `settings_local_template.py` as `settings_local.py` and populate it with your settings.
The `ZOMATO_API_KEY` can be obtained from [here](https://developers.zomato.com/api#headline2).
The `SLACKBOT_API_TOKEN` is the token for bot integration of a new bot to the Slack platform.
It can be obtained from [here](https://my.slack.com/services/new/bot).

## Licence MIT
