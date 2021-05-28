from datetime import datetime
from scrapy.item import Item, Field
from itemloaders.processors import MapCompose


def to_float(text):
    try:
        return float(text)
    except:
        return text


def to_int(text):
    try:
        return int(text)
    except:
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


class HomescrapingItem(Item):

    category = Field(
        input_processor=MapCompose(
            str.strip, str.capitalize)
            )
    page = Field()
    link = Field()
    region = Field() 
    subregion = Field()
    city = Field()
    district = Field()
    latitude = Field()
    longitude = Field()
    title = Field(
        input_processor=MapCompose(str.strip)
            )
    area = Field(
        input_processor=MapCompose(
            str.strip, to_float)
            )
    building_type = Field(
        input_processor=MapCompose(
            str.strip, str.capitalize)
            )
    price = Field(
        input_processor=MapCompose(
        str.strip, to_int)
        )
    price_per_m2 = Field(
        input_processor=MapCompose(
            str.strip, to_int)
            )
    rooms = Field(
        input_processor=MapCompose(
        str.strip, to_int)
    )
    floor = Field(
        input_processor=MapCompose(
        str.strip, to_int)
    )
    market = Field(
        input_processor=MapCompose(
        str.strip, str.capitalize)
    )
    construction_status = Field(
        input_processor=MapCompose(
        str.strip, str.capitalize)
    )
    terrain_type = Field(
        input_processor=MapCompose(
        str.strip, str.capitalize)
    )
    terrain_area = Field(
        input_processor=MapCompose(
        str.strip, to_float)
    )
    build_year = Field(
        input_processor=MapCompose(
        str.strip, to_int)
    )
    oferrer = Field(
        input_processor=MapCompose(
        str.strip, set_oferrer)
    )
    offer_id = Field(
        input_processor=MapCompose(
        str)
    )
    added = Field(
        input_processor=MapCompose(
        str.strip, to_datetime_object)
    )
    last_modified = Field(
        input_processor=MapCompose(
        str.strip, to_datetime_object)
    )
    scraped = Field()
