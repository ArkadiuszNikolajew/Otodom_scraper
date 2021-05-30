import datetime
import json
import logging
import random

import scrapy
import scrapy_splash

from house_scraper import items, loaders
from house_scraper.utils import lua, random_headers
from .config import otodom_settings


class OtodomSpider(scrapy.Spider):

    name = 'otodom'
    base_url = otodom_settings.base_url
    allowed_domains = ['www.otodom.pl',]
    headers = random_headers.RandomHeaders()
    headers.set_site_details(host=allowed_domains[0], referer=base_url)

    def start_requests(self):
        start_urls = otodom_settings.get_start_urls()
        for url in start_urls:
            yield scrapy_splash.SplashRequest(
                url=url, callback=self.parse, headers=self.headers.random_headers, endpoint='execute',
                args={'lua_source': lua.script}
            )

    def parse(self, response):
        # print(response.request)
        offer_links = response.xpath('//h3/a/@href').getall()
        print(offer_links)
        for offer in offer_links:
            yield scrapy_splash.SplashRequest(
                offer, self.parse_offer, headers=self.headers.random_headers, dont_filter=True, endpoint='execute',
                args={'lua_source': lua.script}
            )
        next_page = response.xpath('//ul/li[@class="pager-next"]/a/@href').get()
        if next_page:
            next_page = response.urljoin(next_page)
            yield scrapy_splash.SplashRequest(
                next_page, self.parse, headers=self.headers.random_headers, endpoint='execute',
                args={'lua_source': lua.script}
            )

    def parse_offer(self, response):
        data = json.loads(response.xpath('//script[@id="__NEXT_DATA__"]/text()').get())
        source = data['props']['pageProps']

        item_loader = loaders.OtodomLoader(item=items.HouseScrapingItem(), response=response)

        item_loader.add_value('link', response.url)
        item_loader.add_value('category', source['ad']['category']['name'][0]['value'])
        item_loader.add_value('offer_id', source['ad']['id'])
        item_loader.add_value('title', source['ad']['title'])
        item_loader.add_value('region', source['ad']['location']['geoLevels'][0]['label'])
        item_loader.add_value('subregion',  source['ad']['location']['geoLevels'][1]['label'])
        item_loader.add_value('city', source['ad']['location']['geoLevels'][2]['label'])
        item_loader.add_value('district', source['ad']['location']['geoLevels'][3]['label'])
        item_loader.add_value('latitude', source['ad']['location']['coordinates']['latitude'])
        item_loader.add_value('longitude', source['ad']['location']['coordinates']['longitude'])
        item_loader.add_value('oferrer', source['ad']['advertiserType'])
        item_loader.add_value('added', source['ad']['dateCreated'])
        item_loader.add_value('last_modified', source['ad']['dateModified'])
        item_loader.add_value('scraped', datetime.datetime.now())
        for characteristic in source['ad']['characteristics']:
            if characteristic['key'] == 'price':
                item_loader.add_value('price', characteristic['value'])
            if characteristic['key'] == 'm':
                item_loader.add_value('area', characteristic['value'])
            if characteristic['key'] == 'price_per_m':
                item_loader.add_value('price_per_m2', characteristic['value'])
            if characteristic['key'] == 'rooms_num':
                item_loader.add_value('rooms', characteristic['value'])
            if characteristic['key'] == 'floor_no':
                item_loader.add_value('floor', characteristic['localizedValue'])
            if characteristic['key'] == 'market':
                item_loader.add_value('market', characteristic['localizedValue'])
            if characteristic['key'] == 'building_type':
                item_loader.add_value('building_type', characteristic['localizedValue'])
            if characteristic['key'] == 'construction_status':
                item_loader.add_value('construction_status', characteristic['localizedValue'])
            if characteristic['key'] == 'type':
                item_loader.add_value('terrain_type', characteristic['localizedValue'])
            if characteristic['key'] == 'terrain_area':
                item_loader.add_value('terrain_area', characteristic['value'])
            if characteristic['key'] == 'build_year':
                item_loader.add_value('build_year', characteristic['value'])
        yield item_loader.load_item()
