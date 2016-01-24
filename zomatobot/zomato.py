import datetime

import dateparser
import pyquery
import requests

ACCEPTED_LANGUAGE = 'en,en-US'
USER_AGENT = 'zomato_slack_bot/0.1'


class ZomatoApi:
    def __init__(self, api_key):
        self.__api_key = api_key

    def search(self, query):
        params = {'q': query, 'sort': 'rating', 'order': 'desc'}
        api = 'search'
        response = self.get(api, params)

        return response

    def get(self, api, params):
        headers = {
            'Accept': 'application/json',
            'Accept-Language': ACCEPTED_LANGUAGE,
            'User-Agent': USER_AGENT,
            'user_key': self.__api_key,
        }
        response = requests.get(
                'https://developers.zomato.com/api/v2.1/%s' % api,
                params=params,
                headers=headers
        )

        return response.json()


class DailyMenu:
    def __init__(self, date, items):
        self.date = date
        self.items = items

    def __str__(self):
        items = self.format()
        return 'Menu for {0}\n------------------------------\n{1}\n'.format(self.date, items)

    def __repr__(self):
        return self.__str__()

    def format(self):
        return "\n".join([item.format() for item in self.items])


class MenuItem:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __str__(self):
        return '{} - {}'.format(self.name, self.price)

    def __repr__(self):
        return self.__str__()

    def format(self):
        return '{} _{}_'.format(self.name, self.price)


def lunch_menu(menu_url, date):
    daily_menus = available_lunch_menu(menu_url)

    if date in daily_menus:
        menu = daily_menus[date]
    else:
        menu = None

    return menu


def available_lunch_menu(menu_url):
    div_root = pyquery.PyQuery(menu_url, headers={'User-Agent': USER_AGENT})
    div_menu = div_root('#menu-preview')('.tmi-groups')
    divs_daily_menu = div_menu.items('.tmi-group')
    menu_for_day = {}

    for div_menu in divs_daily_menu:
        weekday_date = _get_trimmed_data(div_menu, '.tmi-group-name').split(', ')
        today_date = datetime.date.today()

        date = dateparser.parse(weekday_date[1]).date()
        date = _fix_year(date, today_date)

        items = []

        divs_items = div_menu.items('.tmi.tmi-daily')
        for div_dish in divs_items:
            name = _get_trimmed_data(div_dish, '.tmi-name')
            price = _get_trimmed_data(div_dish, '.tmi-price.right')

            items.append(MenuItem(name, price))

        menu_for_day[date] = DailyMenu(date, items)

    return menu_for_day


def _fix_year(date, today_date):
    """
    The dates on Zomato site with menus consists only of a month and day. This method is used to determine proper
    year for the date provided. It assumes that the menu displayed was up to date.

    :param date: the date of the menu
    :param today_date: todays date
    :return: a date with day and month set to the same values as the date provided but with corrected year
    """
    today_year = today_date.year
    today_month = today_date.month

    day = date.day
    month = date.month

    if date.month == 12 and today_month == 1:
        year = today_year - 1
    elif date.month == 1 and today_month == 12:
        year = today_year + 1
    else:
        year = today_year

    return datetime.date(year, month, day)


def _get_trimmed_data(node, selector):
    return node(selector).text().strip()
