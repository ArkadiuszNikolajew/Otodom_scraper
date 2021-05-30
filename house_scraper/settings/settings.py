import random
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

BOT_NAME = 'house_scraper'
SPLASH_URL = 'http://localhost:8050'
ROBOTSTXT_OBEY = False
DOWNLOADER_MIDDLEWARES = {
    'scrapy_splash.SplashCookiesMiddleware': 723,
    'scrapy_splash.SplashMiddleware': 725,
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
}
SPIDER_MIDDLEWARES = {
    'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
}
DUPEFILTER_CLASS = 'scrapy_splash.SplashAwareDupeFilter'
HTTPCACHE_STORAGE = 'scrapy_splash.SplashAwareFSCacheStorage'
SPIDER_MODULES = ['house_scraper.spiders.otodom_spider']
NEWSPIDER_MODULE = 'house_scraper.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'house_scraper (+http://www.yourdomain.com)'


# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay

# See also autothrottle settings and docs
DOWNLOAD_DELAY = random.randint(5, 30)

# The download delay setting will honor only one of:
CONCURRENT_REQUESTS_PER_DOMAIN = 1
CONCURRENT_REQUESTS_PER_IP = 5

COOKIES_ENABLED = False

ITEM_PIPELINES = {
   'house_scraper.pipelines.DuplicatesPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
AUTOTHROTTLE_ENABLED = True

# The initial download delay
AUTOTHROTTLE_START_DELAY = 15

# The maximum download delay to be set in case of high latencies
AUTOTHROTTLE_MAX_DELAY = 60

# The average number of requests Scrapy should be sending in parallel to
# each remote server
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0

#Enable showing throttling stats for every response received:
AUTOTHROTTLE_DEBUG = False

FEEDS = {
    '../offers/%(name)s/%(time)s.jsonl': {
        'format': 'jsonlines',
        'encoding': 'utf8',
        'store_empty': False,
        'fields': None,
        'indent': 0,
        'item_export_kwargs': {
            'export_empty_fields': True,
        },
    },
}
