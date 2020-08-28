#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
import itertools
from chibi_requests import Chibi_url

from somos_kudasai import Somos_kudasai
from somos_kudasai.site import somos_kudasai_url
from somos_kudasai.article import Article
from vcr_unittest import VCRTestCase


class Test_kudasai( VCRTestCase ):
    def setUp( self ):
        super().setUp()
        self.main_url = 'https://somoskudasai.com/'
        self.kudasai = Somos_kudasai()


class Test_kudasai_url( Test_kudasai ):
    def test_by_default_should_have_main_page( self ):
        self.assertIn( self.main_url, self.kudasai.url )

    def test_main_url_should_can_be_processing( self ):
        self.assertTrue( self.kudasai.can_proccess( self.main_url ) )

    def test_get_should_work( self ):
        response = self.kudasai.get()
        self.assertTrue( response.native )

    def test_when_create_one_with_main_url_should_use_listado_noticias( self ):
        kudasai = Somos_kudasai( self.main_url )
        self.assertNotEqual( self.main_url, kudasai.url )
        self.assertEqual( somos_kudasai_url, kudasai.url )


class Test_kudasai_handled_page( Test_kudasai ):
    def setUp( self ):
        super().setUp()
        self.kudasai = Somos_kudasai()

    def test_the_last_page_should_be_a_integer( self ):
        self.assertIsInstance( self.kudasai.last_page, int )

    def test_pages_should_be_instances_of_kudasai( self ):
        for page in self.kudasai.pages:
            self.assertIsInstance( page, Somos_kudasai )


class Test_kudasai_get_articles( Test_kudasai ):
    def test_get_article_should_return_instnaces_of_articles( self ):
        page = next( self.kudasai.pages )
        for article in page.articles:
            self.assertIsInstance( article, Article )

    def test_site_should_be_iter_for_articles( self ):
        for article in itertools.islice( self.kudasai, 2 ):
            self.assertIsInstance( article, Article )

    def test_should_work_with_100_articles( self ):
        for article in itertools.islice( self.kudasai, 100 ):
            self.assertIsInstance( article, Article )


class Test_kudasai_append_url( Test_kudasai ):
    def test_append_should_put_in_urls( self ):
        for article in itertools.islice( self.kudasai, 2 ):
            self.kudasai.append( article.url )
        self.assertEqual( len( self.kudasai.urls ), 2 )

    def test_the_urls_should_be_articles( self ):
        for article in itertools.islice( self.kudasai, 2 ):
            self.kudasai.append( article.url )

        for article in self.kudasai.urls:
            self.assertIsInstance( article, Article )

    def test_when_have_urls_should_only_iter_those( self ):
        for article in itertools.islice( self.kudasai, 2 ):
            self.kudasai.append( article.url )

        articles = list( itertools.islice( self.kudasai, 10 ) )

        self.assertEqual( len( articles ), 2 )
        self.assertEqual( articles, self.kudasai.urls )
