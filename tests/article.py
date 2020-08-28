import datetime
import unittest
import itertools
from tests.kudasai import Test_kudasai
from somos_kudasai import Somos_kudasai
from somos_kudasai.site import somos_kudasai_url
from somos_kudasai.article import Article


class Test_article( Test_kudasai ):
    def test_should_get_the_info( self ):
        for article in itertools.islice( self.kudasai, 2 ):
            self.assertIsInstance( article.info, dict )

    def test_info_should_have_the_expected_fields( self ):
        for article in itertools.islice( self.kudasai, 2 ):
            self.assertIn( 'text', article.info )
            self.assertIn( 'title', article.info )
            self.assertIn( 'create_at', article.info )
            self.assertIn( 'author', article.info )

            self.assertIsInstance( article.info.create_at, datetime.datetime )
            self.assertTrue( article.info.text )
            self.assertTrue( article.info.author )
            self.assertTrue( article.info.title )
