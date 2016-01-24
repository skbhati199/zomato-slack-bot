# coding: utf-8

import re

from slackbot.bot import respond_to

import zomatobot.zomato as zomato

ZOMATO_API_KEY = 'd56f96b6a17cd75255e29bb513d67cfc'
ZOMATO_API = zomato.ZomatoApi(ZOMATO_API_KEY)


@respond_to('What is for lunch at (.*)?', re.IGNORECASE)
def todays_menu(message, restaurant_name):
    result = ZOMATO_API.search(restaurant_name)

    if len(result) == 0:
        message.reply('Restaurant not found %s' % restaurant_name)
        return

    restaurant = result['restaurants'][0]['restaurant']

    restaurant_name = restaurant['name']
    restaurant_menu_url = restaurant['menu_url']

    today_lunch_menu = zomato.today_lunch_menu(restaurant_menu_url)

    if today_lunch_menu is None:
        message.reply('There is no lunch served today at %s' % restaurant_name)
        return

    message.reply(str(today_lunch_menu))


@respond_to('Menu at (.*)?', re.IGNORECASE)
def complete_menu(message, restaurant_name):
    result = ZOMATO_API.search(restaurant_name)

    if len(result) == 0:
        message.reply('Restaurant not found %s' % restaurant_name)
        return

    restaurant = result['restaurants'][0]['restaurant']
    restaurant_menu_url = restaurant['menu_url']

    today_lunch_menu = zomato.available_lunch_menu(restaurant_menu_url)

    message.reply("\n\n".join([str(i) for i in today_lunch_menu.values()]))
