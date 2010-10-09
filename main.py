#!/usr/bin/env python
# coding: utf-8


from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.api import memcache
import os
import sys
from google.appengine.ext import db
from google.appengine.ext.webapp import template
from django.utils import simplejson as json
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
import urllib
from google.appengine.api import users

class MainHandler(webapp.RequestHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__), 'views/main.html')
        self.response.out.write(template.render(path, {}))


class AdminHandler(webapp.RequestHandler):
    def get(self):
        
        query = blobstore.BlobInfo.all()
        query.order('-creation')
        blobs = query.fetch(limit=1000)
        template_data = {
            "blobs": blobs,
            "removed": self.request.get("removed", False)
        }
        
        path = os.path.join(os.path.dirname(__file__), 'views/admin.html')
        self.response.out.write(template.render(path, template_data))

class ServeHandler(blobstore_handlers.BlobstoreDownloadHandler):
    def get(self, resource, filename):
        resource = str(urllib.unquote(resource))
        filename = str(urllib.unquote(filename))
        
        blob_info = memcache.get("blob-%s" % resource)
        if blob_info is None:
            blob_info = blobstore.BlobInfo.get(resource)
            memcache.get("blob-%s" % resource, blob_info)
            
        self.send_blob(blob_info)

class NewUploadHandler(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        upload_files = self.get_uploads('file')  # 'file' is file upload field in the form
        blob_info = upload_files[0]
        self.redirect('/manage/ready/%s' % blob_info.key())

class UploadHandler(webapp.RequestHandler):
    def get(self):
        
        template_data = {
            "upload_url": blobstore.create_upload_url('/manage/new')
        }
        
        path = os.path.join(os.path.dirname(__file__), 'views/upload.html')
        self.response.out.write(template.render(path, template_data))

class LogoutHandler(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            self.redirect(users.create_logout_url("/"))
        else:
            self.redirect("/")

class RemoveHandler(webapp.RequestHandler):
    def get(self, resource):
        
        resource = str(urllib.unquote(resource))
        blob_info = blobstore.BlobInfo.get(resource)
        
        blob_info.delete()
        memcache.delete("blob-%s" % resource)
        
        self.redirect('/manage/?removed=true')

class CompleteHandler(webapp.RequestHandler):
    def get(self, resource):
        
        resource = str(urllib.unquote(resource))
        blob_info = blobstore.BlobInfo.get(resource)
        template_data = {
            "blob": blob_info
        }
        
        path = os.path.join(os.path.dirname(__file__), 'views/upload_complete.html')
        self.response.out.write(template.render(path, template_data))

def main():
    application = webapp.WSGIApplication([('/', MainHandler),
                                          ('/serve/([^/]+)/([^/]+)?', ServeHandler),
                                          ('/manage/upload', UploadHandler),
                                          ('/logout', LogoutHandler),
                                          ('/manage/new', NewUploadHandler),
                                          ('/manage/ready/([^/]+)?', CompleteHandler),
                                          ('/manage/remove/([^/]+)?', RemoveHandler),
                                          ('/manage/?', AdminHandler)],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
