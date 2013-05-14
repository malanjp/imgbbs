from wheezy.routing import url
from wheezy.web.handlers import file_handler
from views.views import ListHandler, DetailHandler, DeleteHandler, AboutHandler, ContactHandler

all_urls = [
    url('', ListHandler, name='list'),
    url('page/{page}', ListHandler, name='page'),
    url('detail/{id}', DetailHandler, name='detail'),
    url('reply/{id}', DetailHandler, name='reply'),
    url('delete/{id}', DeleteHandler, name='delete'),
    url('delete/reply/{id}', DeleteHandler, name='delete_reply'),
    url('about', AboutHandler, name='about'),
    url('contact', ContactHandler, name='contact'),
    url('img/{path:any}', file_handler(root='contents/static/upload/'), name='img'),
    url('static/{path:any}', file_handler(root='contents/static/'), name='static')
]
