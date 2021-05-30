import random

from house_scraper.utils.user_agents import edge, opera, chrome, firefox


class RandomHeaders:

    base_accept_header = 'text/html,application/xhtml+xml,application/xml;q=0.9,image'
    all_headers = {
        'Firefox':
            {
                'User-Agent': random.choice(firefox),
                'Accept': base_accept_header + '/webp,*/*;q=0.8',
                'Accept-Language': 'pl,en-US;q=0.7,en;q=0.3',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'Cache-Control': 'max-age=0',
                'TE': 'trailers',

            },
        'Opera':
            {
                'upgrade-insecure-requests': '1',
                'user-agent': random.choice(opera),
                'accept': base_accept_header + '/avif,image/webp,image/apng,*/*;q=0.8,'
                                               'application/signed-exchange;v=b3;q=0.9',
                'sec-ch-ua': '"Chromium"; v = "90", "Opera"; v = "76", ";Not A Brand"; v = "99"',
                'sec-ch-ua-mobile': '?0',
                'sec-fetch-site': 'same-origin',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-user': '?1',
                'sec-fetch-dest': 'document',
                'accept-language': 'pl-PL,pl;q=0.9',
            },
        'Chrome':
            {
                'cache-control': 'max-age=0',
                'upgrade-insecure-requests': '1',
                'user-agent': random.choice(chrome),
                'accept': base_accept_header + '/avif,image/webp,image/apng,*/*;q=0.8,'
                                               'application/signed-exchange;v=b3;q=0.9',
                'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
                'sec-ch-ua-mobile': '?0',
                'sec-fetch-site': 'same-origin',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-user': '?1',
                'sec-fetch-dest': 'document',
                'accept-language': 'pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7',
            },
        'Edge':
            {
                'cache-control': 'max-age=0',
                'upgrade-insecure-requests': '1',
                'user-agent': random.choice(edge),
                'accept': base_accept_header + '/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Microsoft Edge";v="90"',
                'sec-ch-ua-mobile': '?0',
                'sec-fetch-site': 'same-origin',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-user': '?1',
                'sec-fetch-dest': 'document',
                'accept-language': 'pl',
            }
    }

    def __init__(self):
        self.random_headers = random.choice(list(self.all_headers.values()))

    def set_site_details(self, host, referer):
        self.random_headers['host'] = host
        self.random_headers['referer'] = referer
