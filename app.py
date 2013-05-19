from wheezy.http import WSGIApplication
from wheezy.web.middleware import bootstrap_defaults
from wheezy.web.middleware import path_routing_middleware_factory
from wheezy.web.middleware.errors import http_error_middleware_factory
from wheezy.http.middleware import http_cache_middleware_factory
from wheezy.http.config import bootstrap_http_defaults

from config import options
from urls import all_urls
import socket


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
        host = socket.gethostname() 
        print('Visit http://localhost:8080/')
        make_server('', 8080, main).serve_forever()
    except KeyboardInterrupt:
        pass
    print('\nThanks!')

