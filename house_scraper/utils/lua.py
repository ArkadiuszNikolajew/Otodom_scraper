script = '''
    function main(splash)
        splash.http2_enabled = true
        splash.resource_timeout = 20.0
        splash:set_custom_headers(splash.args.headers)
        splash.images_enabled = false
        splash:go{
            url=splash.args.url,
            http_method="GET"
            }
        splash:wait(1)
        return {
            html = splash.html(),
        }
        end
'''