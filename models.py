from google.appengine.ext import ndb

class GuestBook(ndb.Model):
    poimenovanje = ndb.StringProperty()
    posta = ndb.StringProperty()
    besedilo = ndb.StringProperty()
    nastanek = ndb.DateTimeProperty(auto_now_add=True)
    izbris = ndb.BooleanProperty(default=False)
