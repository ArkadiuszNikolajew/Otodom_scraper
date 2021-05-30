from datetime import datetime
from scrapy.item import Item, Field


def serialize_to_int(text):
    try:
        text = int(text)
    except ValueError:
        text = ''
    return text


def serialize_to_float(text):
    try:
        text = float(text)
    except ValueError:
        text = ''
    return text


def set_oferrer(text):
    if text == 'business':
        return 'Biuro nieruchomości'
    elif text == 'private':
        return 'Osoba prywatna'
    else:
        return text


def to_datetime_object(text):
    return datetime.strptime(text, '%Y-%m-%d %H:%M:%S')


class HouseScrapingItem(Item):
    category = Field()
    link = Field()
    region = Field()
    subregion = Field()
    city = Field()
    district = Field()
    latitude = Field(serializer=serialize_to_float)
    longitude = Field(serializer=serialize_to_float)
    title = Field()
    area = Field(serializer=serialize_to_float)
    building_type = Field(serializer=str.capitalize)
    price = Field(serializer=serialize_to_int)
    price_per_m2 = Field(serializer=serialize_to_int)
    rooms = Field(serializer=serialize_to_int)
    floor = Field(serializer=serialize_to_int)
    market = Field(serializer=str.capitalize)
    construction_status = Field(serializer=str.capitalize)
    terrain_type = Field(serializer=str.capitalize)
    terrain_area = Field(serializer=serialize_to_float)
    build_year = Field(serializer=serialize_to_int)
    oferrer = Field(serializer=set_oferrer)
    offer_id = Field()
    added = Field(serializer=to_datetime_object)
    last_modified = Field(serializer=to_datetime_object)
    scraped = Field()
