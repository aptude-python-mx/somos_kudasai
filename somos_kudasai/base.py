# -*- coding: utf-8 -*-
import logging

from chibi.snippet import regex
from chibi.snippet.func import retry_on_exception
from chibi_requests import Chibi_url

from .exceptions import Unexpected_response
from .regex import main_url


logger = logging.getLogger( 'kudasai.base' )


class Site:
    def __init__( self, url=None ):
        self.urls = []
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
                self.urls.append( proccesor( url ) )
                return result

    @staticmethod
    def can_proccess( url ):
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
