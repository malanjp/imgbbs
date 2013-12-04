#import sqlite3
#import mysql.connector
import socket
import pymysql
import pymysql.cursors
from datetime import timedelta
from hashlib import sha1
from wheezy.http import CacheProfile
from wheezy.html.ext.mako import widget_preprocessor
from wheezy.html.ext.template import WhitespaceExtension
from wheezy.html.ext.template import WidgetExtension
from wheezy.html.utils import format_value
from wheezy.html.utils import html_escape
from wheezy.template.engine import Engine
from wheezy.template.ext.core import CoreExtension
from wheezy.template.loader import FileLoader
from wheezy.web.templates import MakoTemplate
from wheezy.web.handlers import file_handler
from wheezy.caching.memory import MemoryCache
from wheezy.caching.patterns import Cached
from wheezy.security.crypto import Ticket
from wheezy.security.crypto.comp import aes128
from wheezy.core.collections import defaultdict


# debug flag
DEBUG = False
if socket.gethostname() == 'ubuntu':
    print('debug mode')
    DEBUG = True


def session():
    if DEBUG:
        return pymysql.connect(db='imgbbs', host='localhost', user='imgbbs', passwd='_WioT.A', charset='utf8')
    else:
        return pymysql.connect(db='imgbbs', host='localhost', user='imgbbs', passwd='_WioT.A', charset='utf8')


# secret key
secretkey = 'faw_iodjnf+ozx90i2j+lkfals1'
static_file = file_handler(root='contents/static/', age=timedelta(hours=1))
template_path = ['contents/templates']
SELECT_LIMIT = 20

# Cache settings
cache = MemoryCache()
cached = Cached(cache, time=15 * 60)
default_cache_profile = CacheProfile('both', duration=60)

# options
options = {
    'render_template': MakoTemplate(
        input_encoding="utf-8",
        directories=template_path,
        filesystem_checks=False,
        preprocessor=[widget_preprocessor]
    ),
    'http_cache': cache,
    'XSRF_NAME': '_x',
    'RESUBMISSION_NAME': '_c',
    'MAX_CONTENT_LENGTH': 1024 * 1024 * 10
}

options.update({
        'CRYPTO_ENCRYPTION_KEY': '_WsoFT.AbI+asdfJ',
        'CRYPTO_VALIDATION_KEY': 'Lf9awLiLAD_SD+ih'
})

options.update({
        'ticket': Ticket(
            max_age=1200,
            salt='Hksdf_df1lka+lA',
            digestmod=sha1),

        'AUTH_COOKIE': '_a',
        'AUTH_COOKIE_DOMAIN': None,
        'AUTH_COOKIE_PATH': '',
        'AUTH_COOKIE_SECURE': False,
})

options['http_errors'] = defaultdict(lambda: 'http500', {
        # HTTP status code: route name
        400: 'http400',
        401: 'signin',
        403: 'http403',
        404: 'http404',
        500: 'http500',
    })






