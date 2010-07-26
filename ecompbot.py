# -*- coding: utf-8 -*-

#Modulos externos
from tools import *
from modules import twitter
from modules import BeautifulSoup

#Modulos padrão
from urllib import urlopen
from time import strftime
from time import sleep

#Modules appengine
#from google.appengine.api import mail
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from models import Noticias

URL = 'http://www.ecomp.poli.br/noticias2.php' # Site das noticias do ECOMP

post_update = twitter.update
    
class NewsException(Exception):
    def __init__(self,msg):
        Exception.__init__(self,msg)

class News():
    def __init__(self,news,date,tag,link=""):

        self.noticia=news.replace('&quote','"')
        self.data = date
        self.tag = u"#"+tag
        self.link = link
        self.id = link.split('=')[-1] # Pega o ID da notica

#'http://www.dsc.upe.br/noticia.php?id=48'
#self.link.split('=')=['http://www.dsc.upe.br/noticia.php?id', '48']

    @property
    def tweet(self):
        self.link = shorter_url(self.link)

        if(not self.is_postable()):
            size = len(self.link) + 10 # O tamanho do link mais alguns caracteres
            self.noticia = self.noticia[:140-size]+"..."
            

        
        return self.__unicode__().encode('utf-8')
        

    def __unicode__(self):
        return unicode(self.noticia)+u'\t %s'%(unicode(self.link))

    def is_postable(self):
        """O limite máximo de uma tweet é 140 caracteres"""
        return len(self)<=140
        
    def __len__(self):
        return len(self.__unicode__())

    def save(self):
        Noticias(identificador=self.id,noticia=self.noticia,tag=self.tag,data=self.data,link=self.link).put()


class MainPage(webapp.RequestHandler):
    def get(self):
        
        hoje = strftime('%d/%m/%Y')
        pagina = urlopen(URL)
        conteudo = BeautifulSoup.BeautifulSoup(pagina.read())#,fromEncoding='utf-8')#'iso-8859-1')
        noticias = my_zip(3,conteudo.findAll('td',{'class':'celula1'}))
        noticias.reverse()
        #<td class="celula1"><a href="http://www.dsc.upe.br/noticia.php?id=57">Problemas no Site do DSC</a></td>
        
        # Aqui é onde a mágica acontece
        for data,texto,tag in noticias[-7:]:  # As 7 primeiras notícias
        
            link = str(texto).split('"')[3]
    
            texto = texto.findAll('a')
            
            data = strip_html(data.string)
            
            tag = strip_html(tag.string)

            if texto:
                texto= strip_html(texto.pop().string)
                
            try:
                
                news=News(texto,data,tag,link)
                print news.noticia.encode('utf-8')
                
                if hoje != news.data and not existe_noticia(news.id):
                    
                    post_update(status = news.tweet)
                    news.save()
                    sleep(1)
                    
            except NewsException,e:
                """mail.send_mail_to_admins(sender='rodrigocliras@gmail.com',
                subject='[ROBOT-ERROR] NoticiaException',
                body='Caro,\n'+str(e))
                """
                pass
            except Exception, e:
                pass
                """
                mail.send_mail_to_admins(sender='rodrigocliras@gmail.com',
                subject='[ROBOT-ERROR] Exception',
                body='Caro,\n'+str(e))
                """

application = webapp.WSGIApplication(
             [('/ecomp',MainPage)],debug=True)

def main():
    run_wsgi_app(application)
    
if __name__ == '__main__':
    main()
