# -*- coding: utf-8 -*-
import logging

from chibi.snippet import regex
from chibi.snippet.func import retry_on_exception
from chibi_requests import Chibi_url

from .exceptions import Unexpected_response
from .regex import main_url


logger = logging.getLogger( 'kudasai.site' )


somos_kudasai_url = 'https://somoskudasai.com/listado-noticias'


class Site:
    def __init__( self, url=None ):
        if not url:
            raise NotImplementedError
        self.url = Chibi_url( url )

    def append( self, url ):
        url = Chibi_url( url )
        if not self.processing_order:
            raise NotImplementedError

        for proccesor in self.processing_order:
            result = proccesor.can_proccess( url )
            if result:
                self.urls.append( result )
                return result

    def can_proccess( self, url ):
        raise NotImplementedError

    @retry_on_exception
    def get( self, *args, url=None, **kw ):
        if url is None:
            url = self.url
        response = url.get()
        if not response.ok:
            raise Unexpected_response
        return response

    @property
    def soup( self ):
        try:
            return self._soup
        except AttributeError:
            response = self.get()
            self._soup = response.native
            return self._soup


class Somos_kudasai( Site ):
    processing_order = []

    def __init__( self, url=None ):
        if not url or self.url_is_main( url ):
            url = somos_kudasai_url
        self.url = Chibi_url( url )

    def can_proccess( self, url ):
        return self.url_is_main( url )

    @staticmethod
    def url_is_main( url ):
        return regex.test( main_url, url )

    @property
    def pages( self ):
        url = self.url
        if not 'page' in url:
            url = url + 'page' + '1'

        yield type( self )( url )
        current_page = int( url.base_name )
        last_page = self.last_page
        dir_url = url.dir_name
        for i in range( current_page, last_page ):
            yield type( self )( dir_url + str( i ) )

    @property
    def last_page( self ):
        pagination = self.soup.find( 'ul', { 'class': 'pagination' } )
        last_page = pagination.find_all( 'a', { 'class': 'page-link' } )[-2]
        return int( last_page.text )

    @property
    def articles( self ):
        articles = self.soup.find_all( 'article' )
        for article in articles:
            link = article.a.attrs[ 'href' ]
            yield self.build_article( link )

    def build_article( self, url ):
        from .article import Article
        return Article( url )

    def __iter__( self ):
        for page in self.pages:
            yield from page.articles
