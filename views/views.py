# vim: set fdm=marker:
import os, re, math
from datetime import timedelta
from PIL import Image
from hashlib import sha1 as sha
from datetime import datetime
import time, random

from wheezy.web.handlers import BaseHandler
from config import DEBUG, session, cached, SELECT_LIMIT, default_cache_profile
from models.upimage import UpImage, Reply
from repositories.upimage import Repository
from validations.upimage import upimage_validator, reply_validator, delete_validator
from wheezy.caching.memory import MemoryCache
from wheezy.http import CacheProfile
from wheezy.http.request import HTTPRequest
from wheezy.http.transforms import gzip_transform
from wheezy.web import handler_cache
from wheezy.web.transforms import handler_transforms
from wheezy.web.handlers.file import FileHandler


class ViewHandler(BaseHandler): #{{{

    def generate_filename(self): #{{{
        d = datetime.today()
        t = time.mktime(d.timetuple())
        r = random.random()
        return sha(r.__str__().encode('utf-8') + t.__str__().encode('utf-8')).hexdigest()
        #}}}

    def imgbbs_preprocess(self, upimage=None): #{{{
        if self.request.files.get('img'):
            img = self.request.files['img'][0]

            if not self.validate_extension(img):
                return self.get(upimage)

            file = img.file
            (filename, thumbname) = self.save_file(file)
            upimage.img = filename
            upimage.thumb = thumbname

        if self.request.form.get('deltime'):
            upimage.deltime = self.request.form.get('deltime')[0].replace('T', ' ')

        return upimage
        #}}}

    def add_commit_object(self, obj, mode=''): #{{{
        con = session()
        repo = Repository(con)
        if mode == '':
          res = repo.add_upimage(obj)
        elif mode == 'reply':
          res = repo.add_reply(obj)
        con.commit()
        return res
        #}}}

    def save_file(self, fieldstrage=None): #{{{
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
            img.save(thumbpath, 'JPEG', quality=50, optimize=True)
        elif ext == 'png':
            img.save(thumbpath, 'PNG', quality=50, optimize=True)
        elif ext == 'gif':
            img = Image.open(filepath, 'r')
            img.save(thumbpath)

        return (filename, thumbname)
        #}}}

    def validate_extension(self, img): #{{{
        pattern = re.compile(r".+\.(jpg|png|gif|jpeg)$", re.IGNORECASE)
        if not pattern.match(img.filename):
            self.error('<div class="alert alert-error">jpg, png, gif いずれかの拡張子でお願いします</div>')
            return False
        return True
        #}}}
#}}}

class ListHandler(ViewHandler): #{{{

    @handler_cache(profile=default_cache_profile)
    @handler_transforms(gzip_transform(compress_level=7, min_length=250))
    def get(self, upimage=None): #{{{
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
        #}}}

    def pagecount(self, count, page): #{{{
        pages = math.ceil(count / SELECT_LIMIT)
        return pages
        #}}}

    def post(self): #{{{
        if not self.validate_xsrf_token():
            return self.redirect_for(self.route_args.route_name)

        upimage = UpImage()
        upimage = self.imgbbs_preprocess(upimage)
        if (not self.try_update_model(upimage)
                or not self.validate(upimage, upimage_validator)):
            print(self.errors)
            return self.get(upimage)

        #if DEBUG:
        #  for key, i in self.request.form.items():
        #    print(key, i)

        con = session()
        repo = Repository(con)
        if not self.add_commit_object(upimage):
            self.error('Sorry, can not add your image.')
            return self.get(upimage)

        cached.dependency.delete('d_list')
        return self.see_other_for('list')
        #}}}
#}}}

class DetailHandler(ViewHandler): #{{{

    @handler_cache(profile=default_cache_profile)
    @handler_transforms(gzip_transform(compress_level=7, min_length=250))
    def get(self, reply=None):
        id = self.route_args.get('id')
        con = session()
        repo = Repository(con)

        upimage = repo.get_upimage(id)
        if not upimage:
            response = self.render_response('errors/http404.mako')
            cached.dependency.delete('d_list')
            cached.dependency.delete('d_detail')
            return response

        replies = repo.get_replies(id)
        reply = reply or Reply()
        if not reply.parent_id:
            reply.parent_id = upimage.id

        response = self.render_response('detail.mako', upimage=upimage, reply=reply, replies=replies)
        response.cache_dependency = ('d_detail', )
        return response

    def post(self):
        if not self.validate_xsrf_token():
            return self.redirect_for(self.route_args.route_name)

        reply = Reply()
        if (not self.try_update_model(reply)
                or not self.validate(reply, reply_validator)):
            print(self.errors)
            return self.get(reply)

        reply = self.imgbbs_preprocess(reply)

        if not reply:
          return self.get(reply)

        if not self.add_commit_object(reply, mode='reply'):
          self.error('Sorry, can not add your image.')
          return self.get(reply)

        cached.dependency.delete('d_detail')
        return self.redirect_for('detail', id=reply.parent_id)
#}}}

class DeleteHandler(ViewHandler): #{{{

    def post(self):
        if not self.validate_xsrf_token():
            return self.redirect_for(self.route_args.route_name)

        if self.route_args.route_name == 'delete': #{{{
            print('delete')
            upimage = UpImage()

            if (not self.try_update_model(upimage)
                    or not self.validate(upimage, delete_validator)):
                return self.redirect_for('detail', id=upimage.id)

            res = self.delete(upimage, mode='upimage')
            if not res:
                response = self.render_response('errors/delkey.mako')
                cached.dependency.delete('d_list')
                cached.dependency.delete('d_detail')
                return response

            cached.dependency.delete('d_detail')
            cached.dependency.delete('d_list')
            response = self.render_response('deleted.mako')
            return response
            #}}}

        if self.route_args.route_name == 'delete_reply': #{{{
            reply = Reply()

            if (not self.try_update_model(reply)
                    or not self.validate(reply, delete_validator)):
                return self.redirect_for('detail', id=reply.parent_id)

            res = self.delete(reply, mode='reply')
            if not res:
                response = self.render_response('errors/delkey.mako')
                cached.dependency.delete('d_list')
                cached.dependency.delete('d_detail')
                return response
            cached.dependency.delete('d_detail')
            return self.redirect_for('detail', id=reply.parent_id)
            #}}}

    def get(self, id=None):
        if id is None:
            return self.redirect_for('list')
        return self.redirect_for('detail', id=id)

    def delete(self, obj=None, mode='upimage'):
        if not obj:
            return False

        filename = self.route_args.get('filename')
        con = session()
        repo = Repository(con)

        delkey = obj.delkey
        if mode == 'upimage':
            obj = repo.get_upimage(id=obj.id)
            obj.delkey = delkey
            res = repo.delete_upimage(obj)
        elif mode == 'reply':
            obj = repo.get_reply(id=obj.id)
            obj.delkey = delkey
            res = repo.delete_reply(obj)
        con.commit()

        if mode == 'upimage':
            res = repo.get_upimage(obj.id)
        elif mode == 'reply':
            res = repo.get_reply(obj.id)
        
        if res:
            return False

        if obj.img:
            os.remove(os.path.join('contents/static/upload/', obj.img))
            os.remove(os.path.join('contents/static/upload/', obj.thumb))

        return True


class SoftwareHandler(ViewHandler):

    @handler_cache(profile=default_cache_profile)
    @handler_transforms(gzip_transform(compress_level=7, min_length=250))
    def get(self):
        response = self.render_response('software.mako')
        response.cache_dependency = ('d_software', )
        return response


class AboutHandler(ViewHandler):

    @handler_cache(profile=default_cache_profile)
    @handler_transforms(gzip_transform(compress_level=7, min_length=250))
    def get(self):
        response = self.render_response('about.mako')
        response.cache_dependency = ('d_about', )
        return response


class ContactHandler(ViewHandler):

    @handler_cache(profile=default_cache_profile)
    @handler_transforms(gzip_transform(compress_level=7, min_length=250))
    def get(self):
        response = self.render_response('contact.mako')
        response.cache_dependency = ('d_contact', )
        return response


class HttpErrorHandler(ViewHandler):

    @handler_cache(profile=default_cache_profile)
    @handler_transforms(gzip_transform(compress_level=7, min_length=250))
    def get(self):
        if self.route_args.route_name == 'http500': #{{{
            response = self.render_response('errors/http500.mako')
            response.cache_dependency = ('d_errors', )
            return response

        if self.route_args.route_name == 'http404': #{{{
            response = self.render_response('errors/http404.mako')
            response.cache_dependency = ('d_errors', )
            return response




