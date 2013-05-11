from wheezy.routing import url
from wheezy.web.handlers import file_handler
from views.views import ListHandler, DetailHandler

all_urls = [
    url('', ListHandler, name='list'),
    url('detail/{filename}', DetailHandler, name='detail'),
    url('static/{path:any}', file_handler(root='contents/static/'), name='static')
]
