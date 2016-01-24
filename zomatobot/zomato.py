# coding: utf-8

import datetime
import re

import dateparser
import pyquery
import requests

USER_AGENT = 'zomato_slack_bot/0.1'


class ZomatoApi:
    def __init__(self, api_key):
        self.__api_key = api_key

    def search(self, query):
        params = {'q': query}
        api = 'search'
        response = self.get(api, params)

        return response

    def get(self, api, params):
        headers = {'user_key': self.__api_key, 'Accept-Language': 'en,en-US;q=0.8,cs;q=0.6,sk;q=0.4',
                   'User-Agent': USER_AGENT,
                   'Accept': 'application/json'}
        response = requests.get(
                'https://developers.zomato.com/api/v2.1/%s' % api,
                params=params,
                headers=headers
        ).json()

        return response


class DailyMenu:
    def __init__(self, date, items):
        self.date = date
        self.items = items

    def __str__(self):
        items = "\n".join([str(i) for i in self.items])
        return 'Menu for {0}\n------------------------------\n{1}\n'.format(self.date, items)

    def __repr__(self):
        return self.__str__()


class MenuItem:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __str__(self):
        return '{} - {}'.format(self.name, self.price)

    def __repr__(self):
        return self.__str__()


def available_lunch_menu(menu_url):
    div_root = pyquery.PyQuery(menu_url, headers={'User-Agent': USER_AGENT})
    div_menu = div_root('#menu-preview')('.tmi-groups')
    divs_daily_menu = div_menu.items('.tmi-group')
    menus = {}
    for div_menu in divs_daily_menu:
        weekday_date = _get_trimmed_data(div_menu, '.tmi-group-name').split(', ')
        date = dateparser.parse(weekday_date[1]).date()

        items = []

        divs_items = div_menu.items('.tmi.tmi-daily')
        for div_dish in divs_items:
            name = _get_trimmed_data(div_dish, '.tmi-name')
            price = _get_trimmed_data(div_dish, '.tmi-price.right')

            items.append(MenuItem(name, price))

        menus[date] = DailyMenu(date, items)

    return menus


def _get_trimmed_data(node, selector):
    return node(selector).text().strip()


def _replace_ignore_case(text, what, to):
    pattern = re.compile(what, re.IGNORECASE)

    return pattern.sub(to, text)


def today_lunch_menu(menu_url):
    today = datetime.datetime.now()

    return lunch_menu(menu_url, today)


def lunch_menu(menu_url, date):
    daily_menus = available_lunch_menu(menu_url)

    if date in daily_menus:
        menu = daily_menus[date]
    else:
        menu = None

    return menu
