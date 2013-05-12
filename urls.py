from wheezy.routing import url
from wheezy.web.handlers import file_handler
from views.views import ListHandler, DetailHandler, AboutHandler, ContactHandler

all_urls = [
    url('', ListHandler, name='list'),
    url('page/{page}', ListHandler, name='page'),
    url('detail/{filename}', DetailHandler, name='detail'),
    url('delete/{filename}', DetailHandler, name='delete'),
    url('about', AboutHandler, name='about'),
    url('contact', ContactHandler, name='contact'),
    url('static/{path:any}', file_handler(root='contents/static/'), name='static')
]
