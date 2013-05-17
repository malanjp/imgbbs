from wheezy.routing import url
from wheezy.http import response_cache
from wheezy.http.transforms import response_transforms, gzip_transform
from wheezy.web.handlers import file_handler
from views.views import ListHandler, DetailHandler, DeleteHandler, SoftwareHandler, AboutHandler, ContactHandler
from config import default_cache_profile
from datetime import timedelta

static_files = response_cache(default_cache_profile)(
    response_transforms(gzip_transform(compress_level=7))(
        file_handler(
            root='contents/static/',
            age=timedelta(hours=1))))

all_urls = [
    url('', ListHandler, name='list'),
    url('page/{page}', ListHandler, name='page'),
    url('detail/{id}', DetailHandler, name='detail'),
    url('reply/{id}', DetailHandler, name='reply'),
    url('delete/{id}', DeleteHandler, name='delete'),
    url('delete/reply/{id}', DeleteHandler, name='delete_reply'),
    url('software', SoftwareHandler, name='software'),
    url('about', AboutHandler, name='about'),
    url('contact', ContactHandler, name='contact'),
    url('img/{path:any}', file_handler(root='contents/static/upload/'), name='img'),
    url('static/{path:any}', static_files, name='static')
]
