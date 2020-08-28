import logging
import datetime
from chibi.atlas import Chibi_atlas
from chibi.snippet import regex
from chibi.snippet.func import retry_on_exception
from chibi_requests import Chibi_url

from .exceptions import Unexpected_response
from .regex import main_url
from .site import Site


logger = logging.getLogger( 'kudasai.article' )


class Article( Site ):
    @property
    def info( self ):
        try:
            return self._info
        except AttributeError:
            self._info = self.parse_info()
            return self._info

    def parse_info( self ):
        article = self.soup.find( 'article' )
        title = article.h1.text
        text = article.div.text
        metas = article.p.find_all( 'span' )
        author = metas[1].text
        date = datetime.datetime.strptime( metas[2].text, '%d/%m/%Y' )
        return Chibi_atlas(
            title=title, text=text, author=author, create_at=date )
