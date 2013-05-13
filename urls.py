from wheezy.routing import url
from wheezy.web.handlers import file_handler
from views.views import ListHandler, DetailHandler, ReplyHandler, DeleteHandler, AboutHandler, ContactHandler

all_urls = [
    url('', ListHandler, name='list'),
    url('page/{page}', ListHandler, name='page'),
    url('detail/{id}', DetailHandler, name='detail'),
    url('reply/{id}', ReplyHandler, name='reply'),
    url('delete/{id}', DeleteHandler, name='delete'),
    url('delete/reply/{id}', DeleteHandler, name='delete_reply'),
    url('about', AboutHandler, name='about'),
    url('contact', ContactHandler, name='contact'),
    url('static/{path:any}', file_handler(root='contents/static/'), name='static')
]
