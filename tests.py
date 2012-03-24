# -*- coding: utf8 -*-

from unittest.case import TestCase
from hamcrest import *
from pyquery import PyQuery as pq

snippets = {}
def save_content(user, key, content):
    snippets[(user, key)] = content

def add_cms_content(dom, key, user, selector="#cms"):
    d = pq(dom)
    d(selector).text(snippets[(user,key)])
    return unicode(d)

class TestCMS(TestCase):
    def setUp(self):
        save_content(user=None, key="HW", content="Hello World")

    def tearDown(self):
        snippets = {}

    def test_simpliest_case(self):
        dom = "<div id='cms'></div>"
        dom_with_cms = add_cms_content(dom, key="HW", user=None)
        assert_that(str(dom_with_cms), is_(equal_to('<div id="cms">Hello World</div>')))

    def test_class_selector(self):
        dom = "<div class='cms'></div>"
        dom_with_cms = add_cms_content(dom, key="HW", user=None, selector=".cms")
        assert_that(dom_with_cms, is_(equal_to('<div class="cms">Hello World</div>')))


class TestCMSAcceptance(TestCase):
    def setUp(self):
        self.dom=u"""<html>
                   <body>
                       <div id="cms">
                       </div>
                       <div id="cms2">
                       </div>
                   <body>
               </html>"""

    def tearDown(self):
        snippets = {}

    def test_simple_acceptance(self):
        user = "user_it"
        user2 = "user_fr"

        save_content(user=user, key="HW", content="Hello World")
        save_content(user=user, key="BJ", content="Bonjourno")
        save_content(user=user2, key="BJ", content="Bonjour")

        dom_with_cms = add_cms_content(self.dom, key="HW", user=user)
        assert_that("Hello World" in dom_with_cms)

        dom_with_cms = add_cms_content(dom_with_cms, key="BJ", user=user, selector="#cms2")
        assert_that("Bonjourno" in dom_with_cms)

        dom_with_cms_fr = add_cms_content(self.dom, key="BJ", user=user2, selector="#cms2")
        assert_that("Bonjour" in dom_with_cms_fr)

    def test_unicode(self):
        user = "user_da"
        save_content(user=user, key="HW", content=u"Høj")

        dom_with_cms = add_cms_content(self.dom, key="HW", user=user)
        assert_that(u"Høj" in dom_with_cms)