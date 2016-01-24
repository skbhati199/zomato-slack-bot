# coding: utf-8

import re
import unicodedata

from slackbot.bot import listen_to
from slackbot.bot import respond_to

import zomatobot.zomato as zomato

ZOMATO_API_KEY = 'd56f96b6a17cd75255e29bb513d67cfc'
ZOMATO_API = zomato.ZomatoApi(ZOMATO_API_KEY)


@listen_to('What is for lunch at (.*)?', re.IGNORECASE)
@respond_to('What is for lunch at (.*)?', re.IGNORECASE)
def todays_menu(message, restaurant_name):
    result = ZOMATO_API.search(restaurant_name)

    if len(result) == 0:
        message.reply('Restaurant \'%s\' was not found' % restaurant_name)
        return

    restaurant = result['restaurants'][0]['restaurant']

    restaurant_name = restaurant['name']
    restaurant_menu_url = restaurant['menu_url']

    today_lunch_menu = zomato.today_lunch_menu(restaurant_menu_url)

    if today_lunch_menu is None:
        message.reply('They do not serve lunch at %s today' % restaurant_name)
        return

    response = strip_accents(str(today_lunch_menu))
    message.reply(response)


@respond_to('Menu at (.*)?', re.IGNORECASE)
@listen_to('Menu at (.*)?', re.IGNORECASE)
def complete_menu(message, restaurant_name):
    result = ZOMATO_API.search(restaurant_name)

    if len(result) == 0:
        message.reply('Restaurant \'%s\' was not found' % restaurant_name)
        return

    restaurant = result['restaurants'][0]['restaurant']
    restaurant_menu_url = restaurant['menu_url']

    today_lunch_menu = zomato.available_lunch_menu(restaurant_menu_url)

    print(today_lunch_menu)

    response = "\n\n".join([str(i) for i in today_lunch_menu.values()])
    response = strip_accents(response)
    message.reply(response)


def strip_accents(text):
    text = unicodedata.normalize('NFD', text)
    text = text.encode('ascii', 'ignore')
    text = text.decode("utf-8")
    return str(text)
