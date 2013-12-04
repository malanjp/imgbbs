from wheezy.http import WSGIApplication
from wheezy.web.middleware import bootstrap_defaults
from wheezy.web.middleware import path_routing_middleware_factory
from wheezy.web.middleware.errors import http_error_middleware_factory
from wheezy.http.middleware import http_cache_middleware_factory
from wheezy.http.config import bootstrap_http_defaults

from config import options, DEBUG
from urls import all_urls
import socket

host = 'localhost'
if DEBUG:
    host = '0.0.0.0'

main = WSGIApplication(
    middleware=[
        bootstrap_defaults(url_mapping=all_urls),
        bootstrap_http_defaults,
        http_cache_middleware_factory,
        http_error_middleware_factory,
        path_routing_middleware_factory
    ],
    options=options)

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    try:
        print('Visit http://{0}:8080/'.format(host))
        make_server(host, 8080, main).serve_forever()
    except KeyboardInterrupt:
        pass
    print('\nThanks!')

