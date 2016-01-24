# Zomato bot for slack

A bot to Slack which can find for you what is for dinner at yout favourite restaurant. If you find it usedful and make some changes please share the changes with us :)

*WARNING - few hours of work*
Unfortunately Zomato does not seem to have an API for daily menu. I used the `pyquery` library to parse the menu from their pages.
Any slight change of their web can break this code.

# How to use it

Copy the `settings_local_template.py` as `settings_local.py` with your settings. The `ZOMATO_API_KEY` can be obtained from [here](https://developers.zomato.com/api#headline2). The `SLACKBOT_API_TOKEN` is the token for bot integration of a new bot to the Slack platform. It can be obtained from [here](https://my.slack.com/services/new/bot).

# Licence MIT
