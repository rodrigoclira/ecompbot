# -*- coding: utf-8 -*-
from google.appengine.ext import db
from string import whitespace

def existe_noticia(identificador):
    """Faz a busca no banco de dados"""
    noticias = db.GqlQuery("SELECT * FROM Noticias WHERE identificador = :1", identificador)
    return noticias.get()!=None
    
class ConexaoException(Exception):
    def __init__(self,msg):
        Exception.__init__(self,msg)
   
def shorter_url(url):
	"""Encurtador de URL"""
	from urllib import urlopen
	try:
		return urlopen("http://is.gd/api.php?longurl=%s" % url).read()
	except:
		raise ConexaoException('Erro ao encurtar a url')

def strip_html(text):
    """Retira as tags"""
    from re import sub
    """
    Remove all html tags from a given string.
    """
    s = sub( '<[^>]*>', '', text).strip(whitespace)
    return s

def my_zip(n,lista):
	"""n é a quantidade de tuplas em que será dividida a lista"""
	if n:
		if len(lista)%n!=0:
			raise Exception("Não é possivel criar tuplas de %d objetos com toda a lista"%n)
		elif  not lista:
			return []
		else:
			t=[]
			x=0
			while x<n:
				t.append(lista.pop(0))
				x+=1
			
		l=[tuple(t)]
		return l + my_zip(n,lista)

	else:
		raise ValueError("Valor n igual a zero")

