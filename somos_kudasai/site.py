# -*- coding: utf-8 -*-
import logging

from chibi.snippet import regex
from chibi.snippet.func import retry_on_exception
from chibi_requests import Chibi_url

from .base import Site
from .exceptions import Unexpected_response
from .regex import main_url
from .article import Article


logger = logging.getLogger( 'kudasai.site' )


somos_kudasai_url = 'https://somoskudasai.com/listado-noticias'


class Somos_kudasai( Site ):
    processing_order = [ Article ]

    def __init__( self, url=None ):
        self.urls = []
        if not url or self.url_is_main( url ):
            url = somos_kudasai_url
        self.url = Chibi_url( url )

    @staticmethod
    def can_proccess( url ):
        return Somos_kudasai.url_is_main( url )

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
        return Article( url )

    def __iter__( self ):
        if not self.urls:
            for page in self.pages:
                yield from page.articles
        else:
            for url in self.urls:
                yield url
