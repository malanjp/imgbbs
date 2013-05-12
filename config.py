import sqlite3
from datetime import timedelta
from hashlib import sha1
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


def session():
    return sqlite3.connect('imgbbs.db',
                           detect_types=sqlite3.PARSE_DECLTYPES)

# secret key
secretkey = 'faw_iodjnf+ozx90i2j+lkfals1'

# Engine settings
static_file = file_handler(root='contents/static/', age=timedelta(hours=1))
searchpath = ['contents/templates']
engine = Engine(
        loader=FileLoader(searchpath),
        extensions=[
            CoreExtension(),
            WhitespaceExtension(),
            WidgetExtension(),
])
SELECT_LIMIT = 20

engine.global_vars.update({
    'format_value': format_value,
    'h': html_escape,
})

# Cache settings
cache = MemoryCache()
cached = Cached(cache, time=15 * 60)


# options
options = {
    'render_template': MakoTemplate(
        input_encoding="utf-8",
        directories=searchpath,
        filesystem_checks=False,
        preprocessor=[widget_preprocessor]
    ),
    'http_cache': cache,
    'XSRF_NAME': '_x',
    'RESUBMISSION_NAME': '_c'
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



