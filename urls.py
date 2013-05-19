from wheezy.routing import url
from wheezy.http import response_cache
from wheezy.web.handlers import file_handler
from views.views import ListHandler, DetailHandler, DeleteHandler, SoftwareHandler, AboutHandler, ContactHandler, HttpErrorHandler
from datetime import timedelta


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
    url('static/{path:any}', file_handler(root='contents/static/', age=timedelta(hours=1)), name='static'),

    # http error code
    url('http400', HttpErrorHandler, name='http400'),
    url('http401', HttpErrorHandler, name='signin'),
    url('http403', HttpErrorHandler, name='http403'),
    url('http404', HttpErrorHandler, name='http404'),
    url('http500', HttpErrorHandler, name='http500'),
]
