import os, re, math
from datetime import timedelta
from PIL import Image
from hashlib import sha1 as sha
import datetime, time, random

from wheezy.web.handlers import BaseHandler
from config import session, cached, SELECT_LIMIT
from models.upimage import UpImage, Reply
from repositories.upimage import Repository
from validations.upimage import upimage_validator, reply_validator
from wheezy.caching.memory import MemoryCache
from wheezy.http import CacheProfile
from wheezy.http.request import HTTPRequest
from wheezy.http.transforms import gzip_transform
from wheezy.web import handler_cache
from wheezy.web.transforms import handler_transforms
from wheezy.web.handlers.file import FileHandler


class ViewHandler(BaseHandler):

    def generate_filename(self):
        d = datetime.datetime.today()
        t = time.mktime(d.timetuple())
        r = random.random()
        return sha(r.__str__().encode('utf-8') + t.__str__().encode('utf-8')).hexdigest()


    def upimage_preprocess(self, upimage=None, request=None):
        if not request.files.get('img'):
            return False

        img = request.files['img'][0]

        if not self.validate_extension(img):
            return self.get(upimage)

        file = img.file
        (filename, thumbname) = self.save_file(file)
        upimage.img = filename
        upimage.thumb = thumbname
        return upimage


    def save_file(self, fieldstrage=None):
        filename = self.generate_filename()
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
        if ext == 'jpg' or ext == 'jpeg':
            img.save(thumbpath, 'JPEG', quality=75, optimize=True)
        elif ext == 'png':
            img.save(thumbpath, 'PNG', quality=75, optimize=True)
        elif ext == 'gif':
            img = Image.open(filepath, 'r')
            img.save(thumbpath)

        return (filename, thumbname)

    def validate_extension(self, img):
        pattern = re.compile(r".+\.(jpg|png|gif|jpeg)$", re.IGNORECASE)
        if not pattern.match(img.filename):
            self.error('<div class="alert alert-error">jpg, png, gif いずれかの拡張子でお願いします</div>')
            return False
        return True


class ListHandler(ViewHandler):

    @handler_transforms(gzip_transform(compress_level=9, min_length=250))
    def get(self, upimage=None):
        page = self.route_args.get('page', 1)

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
            upimage = self.upimage_preprocess(upimage, self.request)

        if (not self.try_update_model(upimage)
                or not self.validate(upimage, upimage_validator)):
            return self.get(upimage)

        con = session()
        repo = Repository(con)
        if not repo.add_upimage(upimage):
            self.error('Sorry, can not add your image.')
            return self.get(upimage)
        con.commit()

        cached.dependency.delete('d_list')
        return self.see_other_for('list')


class DetailHandler(ViewHandler):

    @handler_transforms(gzip_transform(compress_level=9, min_length=250))
    def get(self, reply=None):
        id = self.route_args.get('id')
        con = session()
        repo = Repository(con)

        upimage = repo.get_upimage(id)
        replies = repo.get_reply(id)
        reply = reply or Reply()
        if not reply.parent_id:
            reply.parent_id = upimage.id

        response = self.render_response('detail.mako', upimage=upimage, reply=reply, replies=replies)
        response.cache_dependency = ('d_list', )
        return response

    def post(self):
        if not self.validate_xsrf_token():
            return self.redirect_for(self.route_args.route_name)

        reply = Reply()

        if (not self.try_update_model(reply)):
            return self.redirect_for(self.route_args.route_name)

        reply = self.reply(reply, self.request)
        if reply:
            self.commit_reply(reply)
            return self.redirect_for('detail', id=reply.parent_id)
        else:
            #self.error('<div class="alert alert-error">jpg, png, gif いずれかの拡張子でお願いします</div>')
            return self.get(reply)


    def reply(self, reply=None, request=None):
        if not reply:
            return False

        res = self.upimage_preprocess(reply, self.request)
        if res:
            reply = res

        if (not self.try_update_model(reply)
                or not self.validate(reply, reply_validator)):
            return False

        return reply


    def commit_reply(self, reply):
        con = session()
        repo = Repository(con)
        res = repo.add_reply(reply)
        con.commit()
        return res


class DeleteHandler(ViewHandler):
    def post(self):
        if not self.validate_xsrf_token():
            return self.redirect_for(self.route_args.route_name)

        if self.route_args.route_name == 'delete':
            upimage = UpImage()
            if (not self.try_update_model(upimage)):
                return self.redirect_for(self.route_args.route_name)
            res = self.delete(upimage)
            return self.redirect_for('list')

        if self.route_args.route_name == 'delete_reply':
            reply = Reply()
            if (not self.try_update_model(reply)):
                return self.redirect_for(self.route_args.route_name)
            res = self.delete_reply(reply)
            return self.redirect_for('detail', id=reply.parent_id)


    def get(self):
        return self.redirect_for('list')

    def delete(self, upimage=None):
        if not upimage:
            return False

        if upimage.delkey is '':
            return self.redirect_for(self.route_args.route_name)

        filename = self.route_args.get('filename')
        con = session()
        repo = Repository(con)
        res = repo.delete_upimage(upimage)
        con.commit()
        return res

    def delete_reply(self, reply=None):
        if not reply:
            return False

        if reply.delkey is '':
            return self.redirect_for(self.route_args.route_name)

        filename = self.route_args.get('filename')
        con = session()
        repo = Repository(con)
        res = repo.delete_reply(reply)
        con.commit()
        return res


class SoftwareHandler(ViewHandler):

    @handler_transforms(gzip_transform(compress_level=9, min_length=250))
    def get(self):
        response = self.render_response('software.mako')
        response.cache_dependency = ('d_list', )
        return response


class AboutHandler(ViewHandler):

    @handler_transforms(gzip_transform(compress_level=9, min_length=250))
    def get(self):
        response = self.render_response('about.mako')
        response.cache_dependency = ('d_list', )
        return response


class ContactHandler(ViewHandler):

    @handler_transforms(gzip_transform(compress_level=9, min_length=250))
    def get(self):
        response = self.render_response('contact.mako')
        response.cache_dependency = ('d_list', )
        return response




