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
        seznam = GuestBook.query(GuestBook.izbris == False).fetch()
        podatki = {"seznam":seznam}
        return self.render_template("seznam.html",podatki)

class PosameznoSporociloHandler(BaseHandler):
    def get(self, vnos_id):
        # Iz baze vzamemo sporocilo, katerega id je enak podanemu
        sporocilce = GuestBook.get_by_id(int(vnos_id))

        params = {"posamezno_sporocilce": sporocilce}
        return self.render_template("posamezno_sporocilo.html", params=params)

class UrediHandler(BaseHandler):
    def get(self, vnos_id):
        # Iz baze vzamemo sporocilo, katerega id je enak podanemu
        sporocilce = GuestBook.get_by_id(int(vnos_id))

        params = {"posamezno_sporocilce": sporocilce}
        return self.render_template("uredi_sporocilo.html", params=params)

    def post(self, vnos_id): # to metodo naredimo zaradi shrani gumba
        sporocilce = GuestBook.get_by_id(int(vnos_id)) # potegnemo staro sporocilo iz baze
        sporocilce.poimenovanje = self.request.get("novo-poimenovanje")
        sporocilce.posta = self.request.get("nova-posta")
        sporocilce.besedilo = self.request.get("novo-besedilo")
        sporocilce.put()
        return self.redirect_to("seznam-sporocil")

class DeleteHandler(BaseHandler):
    def get(self, vnos_id):
        # Iz baze vzamemo sporocilo, katerega id je enak podanemu
        sporocilce = GuestBook.get_by_id(int(vnos_id))
        params = {"posamezno_sporocilce": sporocilce}
        return self.render_template("izbrisi_sporocilo.html", params=params)

    def post(self, vnos_id):
        sporocilce = GuestBook.get_by_id(int(vnos_id))  # potegnemo staro sporocilo iz baze
        sporocilce.izbris = True
        sporocilce.put()
        return self.redirect_to("seznam-sporocil")

class KosHandler (BaseHandler):
    def get(self):
        kos_seznam = GuestBook.query(GuestBook.izbris == True).fetch()
        podatki = {"kos_seznam":kos_seznam}
        return self.render_template("kos_seznam.html",podatki)

class EternalDeleteHandler (BaseHandler):
    def get(self, vnos_id):
        # Iz baze vzamemo sporocilo, katerega id je enak podanemu
        sporocilce = GuestBook.get_by_id(int(vnos_id))
        params = {"posamezno_sporocilce": sporocilce}
        return self.render_template("unici_sporocilo.html", params=params)

    def post(self, vnos_id):
        sporocilce =  GuestBook.get_by_id(int(vnos_id))
        sporocilce.key.delete()
        return self.redirect_to("kos-sporocil")

class ObnoviHandler (BaseHandler):
    def get(self, vnos_id):
        # Iz baze vzamemo sporocilo, katerega id je enak podanemu
        sporocilce = GuestBook.get_by_id(int(vnos_id))
        params = {"posamezno_sporocilce": sporocilce}
        return self.render_template("obnovi_sporocilo.html", params=params)

    def post(self, vnos_id):
        sporocilce = GuestBook.get_by_id(int(vnos_id))  # potegnemo staro sporocilo iz baze
        sporocilce.izbris = False
        sporocilce.put()
        return self.redirect_to("seznam-sporocil")

app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/rezultat', RezultatHandler),
    webapp2.Route('/seznam', ListHandler, name="seznam-sporocil"),
    webapp2.Route('/sporocilo/<vnos_id:\d+>', PosameznoSporociloHandler),
    webapp2.Route('/sporocilo/<vnos_id:\d+>/edit', UrediHandler),
    webapp2.Route('/sporocilo/<vnos_id:\d+>/delete', DeleteHandler),
    webapp2.Route('/kos', KosHandler, name="kos-sporocil"),
    webapp2.Route('/sporocilo/<vnos_id:\d+>/destroy', EternalDeleteHandler),
    webapp2.Route('/sporocilo/<vnos_id:\d+>/renew', ObnoviHandler),
], debug=True)
