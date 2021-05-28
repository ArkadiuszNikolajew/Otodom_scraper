script = '''
    function main(splash)
        splash.resource_timeout = 10
        splash:set_custom_headers(splash.args.headers)
        splash.images_enabled = false
        splash:go{
            url=splash.args.url,
            }
        splash:wait(1)
        return {
            html = splash.html(),
        }
        end
'''