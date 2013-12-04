# vim: set fdm=marker:
import os, re, math
from datetime import timedelta
from PIL import Image
from hashlib import sha1 as sha
from datetime import datetime
import time, random
import feedgenerator

from wheezy.web.handlers import BaseHandler
from config import DEBUG, session, cached, SELECT_LIMIT, default_cache_profile
from models.upimage import UpImage, Reply
from repositories.upimage import Repository
from validations.upimage import upimage_validator, reply_validator, delete_validator
from wheezy.caching.memory import MemoryCache
from wheezy.http import CacheProfile, HTTPResponse
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

    def imgbbs_preprocess(self, upimage=None, img=None): #{{{
        if not self.validate_extension(img):
            return self.get(upimage)

        (filename, thumbname) = self.save_file(img)
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

    def save_file(self, img=None): #{{{
        filename = self.generate_filename()
        file = img.file
        ext = img.filename.split('.')[-1].lower()
        print(ext)
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

    #@handler_cache(profile=default_cache_profile)
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
        print(self.request.environ)
        if not self.validate_xsrf_token():
            return self.redirect_for(self.route_args.route_name)

        upimage = UpImage()
        if not self.request.files.get('img[]'):
            if (not self.try_update_model(upimage)
                    or not self.validate(upimage, upimage_validator)):
                cached.dependency.delete('d_list')
                return self.get(upimage)

        count = len(self.request.files['img[]'])
        for idx, img in enumerate(self.request.files['img[]']):
            upimage = self.imgbbs_preprocess(upimage, img)
            if (not self.try_update_model(upimage)
                    or not self.validate(upimage, upimage_validator)):
                return self.get(upimage)

            con = session()
            repo = Repository(con)

            # スレ立てる
            if idx == 0:
                upimage = self.add_commit_object(upimage)
                if not upimage:
                    self.error('Sorry, can not add your image.')
                    cached.dependency.delete('d_list')
                    return self.get(upimage)
                thread_id = upimage.id

            # 画像が複数件あるなら立てたスレにレスの形で残りをうｐ
            if idx > 0 and count > 1:
                upimage.parent_id = thread_id
                if not self.add_commit_object(upimage, mode='reply'):
                    self.error('Sorry, can not add your image.')
                    cached.dependency.delete('d_detail')
                    cached.dependency.delete('d_list')
                    return self.get(reply)

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

        print(self.request.form)
        reply = Reply()
        if (not self.try_update_model(reply)
                or not self.validate(reply, reply_validator)):
            print(self.errors)
            cached.dependency.delete('d_detail')
            return self.get(reply)

        imgs = self.request.files.get('img[]')
        if imgs:
            count = len(imgs)
            for idx, img in enumerate(imgs):
                reply = self.imgbbs_preprocess(reply, img)

                if (not self.try_update_model(reply)
                        or not self.validate(reply, reply_validator)):
                    return self.get(reply)

                if not reply:
                    cached.dependency.delete('d_detail')
                    return self.get(reply)

                if not self.add_commit_object(reply, mode='reply'):
                    self.error('Sorry, can not add your image.')
                    cached.dependency.delete('d_detail')
                    return self.get(reply)

        cached.dependency.delete('d_detail')
        cached.dependency.delete('d_list')
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
#}}}

class SoftwareHandler(ViewHandler): #{{{

    @handler_cache(profile=default_cache_profile)
    @handler_transforms(gzip_transform(compress_level=7, min_length=250))
    def get(self):
        response = self.render_response('software.mako')
        response.cache_dependency = ('d_software', )
        return response
#}}}

class AboutHandler(ViewHandler): #{{{

    @handler_cache(profile=default_cache_profile)
    @handler_transforms(gzip_transform(compress_level=7, min_length=250))
    def get(self):
        response = self.render_response('about.mako')
        response.cache_dependency = ('d_about', )
        return response
#}}}

class ContactHandler(ViewHandler): #{{{

    @handler_cache(profile=default_cache_profile)
    @handler_transforms(gzip_transform(compress_level=7, min_length=250))
    def get(self):
        response = self.render_response('contact.mako')
        response.cache_dependency = ('d_contact', )
        return response
#}}}

class AtomHandler(ViewHandler): #{{{

    #@handler_cache(profile=default_cache_profile)
    @handler_transforms(gzip_transform(compress_level=7, min_length=250))
    def get(self):
        con = session()
        repo = Repository(con)

        CONTENT_TYPE_XML='text/xml'
        CONTENT_TYPE_XML_RSP=CONTENT_TYPE_XML+'; charset=utf-8'

        if DEBUG:
            base_url = 'http://192.168.72.100:8080'
        else:
            base_url = 'http://shoboi.net'

        feed = feedgenerator.Atom1Feed(
            title = 'しょぼいろだ。',
            link = 'http://shobi.net/',
            feed_url = 'http://shoboi.net/atom',
            description = u'エロも笑いも虹も惨事もしょぼいろだで共有してね',
            author_name=u'しょぼい。',
            language = u"ja",
            pubdate = datetime.utcnow()
        )

        upimages = repo.list_upimages()
        for idx, i in enumerate(upimages):
            feed.add_item(
                title = i.title or 'タイトルなし',
                link = '%s/detail/%s' % (base_url, i.id),
                description = """<![CDATA[
                    <a href="%s/detail/%s">
                      <img src="%s/img/%s">
                    </a>
                ]]>""" % (base_url, i.id, base_url, i.thumb),
                author_name = i.author or '名無し',
                pubdate = datetime.now()
            )
            if idx >= 4: # 5件まで
                break;

        response = HTTPResponse()
        content_type = ('Content-Type', CONTENT_TYPE_XML_RSP)
        response.headers[0] = content_type
        response.write(feed.writeString('utf-8'))
        response.cache_dependency = ('d_atom', )
        return response
#}}}

class HttpErrorHandler(ViewHandler): #{{{

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
#}}}



