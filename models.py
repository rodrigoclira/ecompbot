#!/usr/bin/env python
from google.appengine.ext import db
class Noticias(db.Model):
    identificador = db.StringProperty()
    noticia = db.StringProperty()
    data = db.StringProperty()
    tag = db.StringProperty()
    link = db.StringProperty()