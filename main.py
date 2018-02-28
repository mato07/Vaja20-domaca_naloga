#!/usr/bin/env python
import os
import jinja2
import webapp2
from models import GuestBook


template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=True)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if params is None:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        return self.render_template("home.html")

class RezultatHandler(BaseHandler):
    def post(self):

        imeinupriimek = self.request.get("imepriimek")
        email3 = self.request.get("email")
        message2 = self.request.get("sporocilo")

        if not imeinupriimek:
            imeinupriimek = "neznanec"

        gost = GuestBook(poimenovanje=imeinupriimek, posta=email3, besedilo=message2)

        gost.put()

        podatki={"namesurname": imeinupriimek,
                 "email2": email3,
                 "message": message2}
        return self.render_template("rezultat.html",podatki)

class ListHandler(BaseHandler):
    def get(self):
        seznam = GuestBook.query().fetch()
        podatki = {"seznam":seznam}
        return self.render_template("seznam.html",podatki)

app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/rezultat', RezultatHandler),
    webapp2.Route('/seznam', ListHandler),
], debug=True)
