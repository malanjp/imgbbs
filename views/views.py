import os, re
from datetime import timedelta
import math
from PIL import Image

from wheezy.web.handlers import BaseHandler
from config import session, cached, SELECT_LIMIT
from models.upimage import UpImage
from repositories.upimage import Repository
from validations.upimage import upimage_validator
from wheezy.caching.memory import MemoryCache
from wheezy.http import CacheProfile
from wheezy.http.request import HTTPRequest
from wheezy.http.transforms import gzip_transform
from wheezy.web import handler_cache
from wheezy.web.transforms import handler_transforms
from wheezy.web.handlers.file import FileHandler



class ListHandler(BaseHandler):

    @handler_transforms(gzip_transform(compress_level=9, min_length=250))
    def get(self, upimage=None):
        page = self.route_args.get('page', 1)

        #with session() as db:
        con = session()
        repo = Repository(con)

        count = repo.get_count()
        pages = self.pagecount(count, SELECT_LIMIT)

        upimages = repo.list_upimages(page)   # list
        upimage = upimage or UpImage()   # add form

        response = self.render_response('list.mako',
                upimages=upimages, upimage=upimage, count=count, page=page, pages=pages)
        response.cache_dependency = ('d_list', )
        return response

    def pagecount(self, count, page):
        pages = math.ceil(count / SELECT_LIMIT)
        return pages

    def post(self):
        if not self.validate_xsrf_token():
            return self.redirect_for(self.route_args.route_name)

        upimage = UpImage()

        if 'img' in self.request.files:
            img = self.request.files['img'][0]

            print(img.filename)
            pattern = re.compile(r".+\.(jpg|png|gif|jpeg)$", re.IGNORECASE)
            if not pattern.match(img.filename):
                self.error('<div class="alert alert-error">jpg, png, gif いずれかの拡張子でお願いします</div>')
                return self.get(upimage)

            file = img.file
            (filename, thumbname) = self.save_file(file)
            upimage.img = filename
            upimage.thumb = thumbname

        if (not self.try_update_model(upimage)
                or not self.validate(upimage, upimage_validator)):
            return self.get(upimage)
        print(upimage.title)

        #with session() as db:
        con = session()
        repo = Repository(con)
        if not repo.add_upimage(upimage):
            self.error('Sorry, can not add your image.')
            return self.get(upimage)
        con.commit()

        cached.dependency.delete('d_list')
        return self.see_other_for('list')

    def save_file(self, fieldstrage=None):
        from hashlib import sha1 as sha
        import datetime, time, random
        d = datetime.datetime.today()
        t = time.mktime(d.timetuple())
        r = random.random()
        filename = sha(r.__str__().encode('utf-8') + t.__str__().encode('utf-8')).hexdigest()

        img = self.request.files['img'][0]
        file = img.file
        ext = img.filename.split('.')[-1]
        thumbname =  filename + '_thumb.' + ext
        filename =  filename + '.' + ext
        thumbpath = os.path.join('contents/static/upload/', thumbname)
        filepath = os.path.join('contents/static/upload/', filename)
        open(filepath, 'wb').write(file.read())

        # create thumbnail
        img = Image.open(filepath, 'r')
        img.thumbnail((200, 170), Image.ANTIALIAS)
        img.save(thumbpath, 'JPEG', quality=75, optimize=True)

        return (filename, thumbname)


class DetailHandler(BaseHandler):

    @handler_transforms(gzip_transform(compress_level=9, min_length=250))
    def get(self, filename=None):
        filename = self.route_args['filename']
        #with session() as db:
        con = session()
        repo = Repository(con)
        upimage = repo.get_upimages(filename)
        response = self.render_response('detail.mako', upimage=upimage)
        response.cache_dependency = ('d_list', )
        return response

    def post(self):
        if not self.validate_xsrf_token():
            return self.redirect_for(self.route_args.route_name)

        upimage = UpImage()
        if (not self.try_update_model(upimage)):
            return self.redirect_for(self.route_args.route_name)

        if upimage.delkey is '':
            return self.redirect_for(self.route_args.route_name)

        filename = self.route_args['filename']
        #with session() as db:
        con = session()
        repo = Repository(con)
        res = repo.delete_upimages(upimage)
        if res:
            return self.redirect_for('list')
        else:
            return self.redirect_for(self.route_args.route_name)


class AboutHandler(BaseHandler):

    @handler_transforms(gzip_transform(compress_level=9, min_length=250))
    def get(self):
        response = self.render_response('about.mako')
        response.cache_dependency = ('d_list', )
        return response


class ContactHandler(BaseHandler):

    @handler_transforms(gzip_transform(compress_level=9, min_length=250))
    def get(self):
        response = self.render_response('contact.mako')
        response.cache_dependency = ('d_list', )
        return response




