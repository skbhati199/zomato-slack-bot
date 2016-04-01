import datetime as dt
import json
import re
import unicodedata

import dateparser
from slackbot.bot import listen_to
from slackbot.bot import respond_to

import settings_local
import zomatobot.zomato as zomato

ZOMATO_API = zomato.ZomatoApi(settings_local.ZOMATO_API_KEY)


@listen_to('Today\'s menu at (.*)\\?', re.IGNORECASE)
@respond_to('(.*)', re.IGNORECASE)
def todays_menu(message, query_str):
    handle_menu_request(message, query_str, dt.date.today())


@listen_to('What is for lunch at (.*) on (.*)\\?', re.IGNORECASE)
def menu_for_dat(message, query_str, date_str):
    date = dateparser.parse(date_str).date()

    handle_menu_request(message, query_str, date)


def handle_menu_request(message, query, date):
    result = ZOMATO_API.search(query)

    if not result or not result['restaurants']:
        message.reply('No restaurant found for these keywords: \'%s\'' % query)
        return

    restaurant = result['restaurants'][0]['restaurant']
    menu_url = restaurant['menu_url']
    lunch_menu = zomato.lunch_menu(menu_url, date)

    if lunch_menu is None:
        attachments = __restaurant_info_attachment(restaurant)

        if date is dt.date.today():
            message.send_webapi('No menu found for today' % attachments)
        else:
            message.send_webapi('No menu found for %s' % date, attachments)

    else:
        attachments = __restaurant_menu_attachment(restaurant, lunch_menu)
        message.send_webapi('Look what I found for you!', attachments)


def __restaurant_info_attachment(restaurant):
    name = restaurant['name']
    menu_url = restaurant['menu_url']
    logo_url = restaurant['thumb']
    fields = __restaurant_info_fields(restaurant)

    attachment = {
        "fallback": 'Link to the %s\'s menu page - %s' % (name, menu_url),
        "title": '%s\'s menu page' % name,
        "title_link": menu_url,
        "thumb_url": logo_url,
        "text": 'Link to the restaurants\'s menu page',
        'color': '#DD0000',
        "fields": fields
    }

    return json.dumps([attachment])


def __restaurant_menu_attachment(restaurant, menu):
    name = restaurant['name']
    menu_url = restaurant['menu_url']
    logo_url = restaurant['thumb']
    fields = __restaurant_info_fields(restaurant)

    date = menu.date
    items = __strip_accents(menu.format())

    attachment = {
        "fallback": '%s\'s menu for the %s - %s' % (name, date, menu_url),
        "title": '%s\'s menu for %s' % (name, menu.date),
        "title_link": menu_url,
        "thumb_url": logo_url,
        "text": items,
        'color': '#DD0000',
        "fields": fields
    }

    return json.dumps([attachment])


def __restaurant_info_fields(restaurant):
    fields = []
    if 'location' in restaurant:
        location = restaurant['location']

        if 'address' in location:
            address = location['address']

            fields.append({
                "title": "Address",
                "value": address,
                "short": True
            })

    if 'user_rating' in restaurant:
        user_rating = restaurant['user_rating']

        if 'aggregate_rating' in user_rating and 'rating_text' in user_rating:
            aggregate_rating = user_rating['aggregate_rating']
            rating_text = user_rating['rating_text']

            fields.append({
                "title": "Rating",
                "value": "%s - %s" % (aggregate_rating, rating_text),
                "short": True
            })

    return fields


def __strip_accents(text):
    text = str(text)
    text = unicodedata.normalize('NFD', text)
    text = text.encode('ascii', 'ignore')
    text = text.decode("utf-8")
    return str(text)
