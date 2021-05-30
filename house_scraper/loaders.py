from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst, MapCompose


class OtodomLoader(ItemLoader):

    default_input_processor = MapCompose(str, str.strip)
    default_output_processor = TakeFirst()