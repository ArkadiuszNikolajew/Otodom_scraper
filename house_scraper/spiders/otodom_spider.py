import scrapy
import scrapy_splash
import random
import datetime
import json

# import os


from house_scraper import items, headers, loaders, lua


class OtodomSpider(scrapy.Spider):

    name = 'otodom'
    base_url = 'https://www.otodom.pl'
    allowed_domains = ['www.otodom.pl',]
    headers.referer = base_url
    headers.host = allowed_domains[0]
    headers = random.choice(headers.headers)
     

    def start_requests(self):
        start_urls = [
            self.base_url + '/sprzedaz/mieszkanie/jelenia-gora/?search%5Bcreated_since%5D=14&search%5Bregion_id%5D=1&search%5Bsubregion_id%5D=58&search%5Bcity_id%5D=182&search%5Bdist%5D=25',
            self.base_url + '/sprzedaz/dom/jelenia-gora/?search%5Bcreated_since%5D=14&search%5Bregion_id%5D=1&search%5Bsubregion_id%5D=58&search%5Bcity_id%5D=182&search%5Bdist%5D=25',
            self.base_url + '/sprzedaz/dzialka/jelenia-gora/?search%5Bcreated_since%5D=14&search%5Bregion_id%5D=1&search%5Bsubregion_id%5D=58&search%5Bcity_id%5D=182&search%5Bdist%5D=25'
            ]
        
        for url in start_urls:
            yield scrapy_splash.SplashRequest(url, self.parse, headers=self.headers, endpoint='execute', args={'lua_source': lua.script})

    def parse(self, response):
        self.headers['referer'] = 'https://www.otodom.pl/sprzedaz/jelenia-gora/?search%5Bregion_id%5D=1&search%5Bsubregion_id%5D=58&search%5Bcity_id%5D=182&search%5Bdist%5D=25'
        offer_links = response.xpath('//h3/a/@href').getall()
        for offer in offer_links:
            yield scrapy_splash.SplashRequest(offer, self.parse_offer, headers=self.headers, dont_filter=True, endpoint='execute', args={'lua_source': lua.script})

        next_page = response.xpath('//ul/li[@class="pager-next"]/a/@href').get()
        if next_page:
            next_page = response.urljoin(next_page)
            yield scrapy_splash.SplashRequest(next_page, self.parse, headers=self.headers, endpoint='execute', args={'lua_source': lua.script})
            

    
    def parse_offer(self, response):
        data = json.loads(response.xpath('//script[@id="__NEXT_DATA__"]/text()').get())
        
        source = data['props']['pageProps']
        
        item_loader = loaders.OtodomLoader(item=items.HomescrapingItem(), response=response)
        item_loader.add_value('category', source['ad']['target']['ProperType'])
        item_loader.add_value('link', response.url)
        item_loader.add_value('page', source['siteConfig']['tracking']['siteUrl'])
        item_loader.add_value('region', source['ad']['location']['geoLevels'][0]['label'])
        item_loader.add_value('subregion',  source['ad']['location']['geoLevels'][1]['label'])
        item_loader.add_value('city', source['ad']['location']['geoLevels'][2]['label'])
        item_loader.add_value('district', source['ad']['location']['geoLevels'][3]['label'])
        item_loader.add_value('latitude', source['ad']['location']['coordinates']['latitude'])
        item_loader.add_value('longitude', source['ad']['location']['coordinates']['longitude'])
        item_loader.add_value('title', source['ad']['title'])

        for char in source['ad']['characteristics']:
            if char['key'] == 'price':
                item_loader.add_value('price', char['value'])
            if char['key'] == 'm':
                item_loader.add_value('area', char['value'])
            if char['key'] == 'price_per_m':
                item_loader.add_value('price_per_m2', char['value'])
            if char['key'] == 'rooms_num':
                item_loader.add_value('rooms', char['value'])
            if char['key'] == 'floor_no':
                item_loader.add_value('floor', char['localizedValue'])
            if char['key'] == 'market':
                item_loader.add_value('market', char['localizedValue'])
            if char['key'] == 'building_type':
                item_loader.add_value('building_type', char['localizedValue'])
            if char['key'] == 'construction_status':
                item_loader.add_value('construction_status', char['localizedValue'])
            if char['key'] == 'type':
                item_loader.add_value('terrain_type', char['localizedValue'])
            if char['key'] == 'terrain_area':
                item_loader.add_value('terrain_area', char['value'])
            if char['key'] == 'build_year':
                item_loader.add_value('build_year', char['value'])

        item_loader.add_value('oferrer', source['ad']['advertiserType'])
        item_loader.add_value('offer_id', source['ad']['id'])
        item_loader.add_value('added', source['ad']['dateCreated'])
        item_loader.add_value('last_modified', source['ad']['dateModified'])
        item_loader.add_value('scraped', datetime.datetime.now())

        yield item_loader.load_item()
        
