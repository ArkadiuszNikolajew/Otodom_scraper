import unicodedata
import yaml
from urllib import parse
from house_scraper.settings.settings import BASE_DIR


class OtodomSpiderSettings:

    base_url = 'https://www.otodom.pl/'

    def __init__(self):
        with open(BASE_DIR / 'settings/setup.yml', 'r') as setup_file:
            self.settings = yaml.safe_load(setup_file)['otodom_filters']
        self.start_urls = []

    def urlize_city(self):
        city_name = self.settings.get('city_name')
        if city_name:
            return unicodedata.normalize('NFKD', city_name)\
                .strip()\
                .lower()\
                .replace(' ', '-')\
                .replace(u'ł', 'l')\
                .encode('ascii', 'ignore')\
                .decode('utf-8') + '/'

    def urlize_offer_type(self):
        offer_type = self.settings.get('offer_type')
        if offer_type == 'sprzedaz' or offer_type == 'wynajem':
            return f'{offer_type}/'
        return 'sprzedaz/'

    def urlize_created_since(self):
        created_since = self.settings.get('created_since')
        if created_since:
            return '&' + f'{parse.quote("search[created_since]")}' + f'={created_since}'

    def urlize_distance(self):
        distance = self.settings.get('distance')
        if distance:
            return '&' + f'{parse.quote("search[dist]")}' + f'={distance}'

    def get_start_urls(self):
        categories = self.settings.get('categories')

        if categories:
            self.start_urls = [
                f'{self.base_url}{self.urlize_offer_type()}{category}/{self.urlize_city()}?'
                f'{self.urlize_created_since()}{self.urlize_distance()}'
                for category in categories]
        else:
            self.start_urls.append(
                f'{self.base_url}{self.urlize_offer_type()}{self.urlize_city()}?'
                f'{self.urlize_created_since()}{self.urlize_distance()}')
        return self.start_urls


otodom_settings = OtodomSpiderSettings()





