# -*- coding: utf-8 -*-


from unittest.case import TestCase
from hamcrest import *
from hamcrest.core.base_matcher import BaseMatcher
import re

from cms_processor import add_content_type, add_content, add_cms_contain, apply_layout, validate_layout
from models import ContentType, Content

class ContentTypeTest(TestCase):

    def test_register_content_type(self):
        add_content_type(type="news", user="fangiot", layout="<>", selector="kd")
        assert_that(ContentType.objects.count(), is_(1))

    def test_invalid_layout_raise_exception(self):
        with self.assertRaises(ValueError):
            add_content_type(type="news", user="fangiot", layout="{{ other }}", selector="kd")

    def test_validate_layout(self):
        assert_that(validate_layout("{{ other }}"), is_(False))
        assert_that(validate_layout("{{ contents }}"), is_(True))
        assert_that(validate_layout("{% for content in other %}{% enfor %}"), is_(False))

    def test_register_content(self):
        add_content_type(type="content", user="fangiot", layout="<>", selector="kd")
        add_content(user="fangiot", type="content", content="my content")
        assert_that(Content.objects.filter(type="content").count(), is_(1))

    def test_get_content_for_page(self):
        add_content_type(type="infos", user="fangiot", layout="<p>{{content}}</p>", selector="#infos", unique=True)
        add_content_type(type="other", user="fangiot", layout="<p>{{content}}</p>", selector="#other")
        add_content(user="fangiot", type="infos", content=u"Something happened hÉ")
        add_content(user="fangiot", type="other", content=u"Other")

        assert_that(add_cms_contain(user="fangiot", page="<div id='infos'></div>"), is_(u'<div id="infos"><p>Something happened hÉ</p></div>'))
        assert_that(add_cms_contain(user="fangiot", page='<div id="news">my news</div>'), is_(u'<div id="news">my news</div>'))


    def test_layout(self):
        assert_that(apply_layout(layout="", content=""), is_(""))
        assert_that(apply_layout(layout="", content="Content"), is_(""))
        assert_that(apply_layout(layout="<p></p>", content="Content"), is_("<p></p>"))
        assert_that(apply_layout(layout="<p>{{ content }}</p>", content=""), is_("<p></p>"))
        assert_that(apply_layout(layout="<p>{{ content }}</p>", content="Content"), is_("<p>Content</p>"))
        assert_that(apply_layout(layout="<p>{{ other }}</p>", content="Content"), is_("<p></p>"))
        assert_that(apply_layout(layout="{% for content in contents %}<p>{{ content }}</p>{% endfor %}", contents=["Content"]), is_("<p>Content</p>"))
        assert_that(apply_layout(layout="{% for content in contents %}<p>{{ content }}</p>{% endfor %}", contents=["Content1", "Content2"]), is_("<p>Content1</p><p>Content2</p>"))


    def tearDown(self):
        ContentType.objects.delete()
        Content.objects.delete()

class CMSTest(TestCase):

    def tearDown(self):
        ContentType.objects.delete()
        Content.objects.delete()

    def test_add_a_newslist(self):
        user = "fangiot"
        page = """<html>
                    <body>
                        <h1>My personnel page</h1>

                        <h2>My information</h2>
                        <p>I am Anthony</p>

                        <div id="newslist"></div>
                    </body>
                  </html>"""

        expected_page = u"""<html>
                    <body>
                        <h1>My personnel page</h1>

                        <h2>My information</h2>
                        <p>I am Anthony</p>

                        <div id="newslist">
                            <ul>
                                <li>I am happy</li>
                                <li>Woaw, wonderful day!</li>
                            </ul>
                        </div>
                    </body>
                  </html>"""


        layout = """<ul>
                        {% for content in contents %}
                            <li>{{ content }}</li>
                        {% endfor %}
                    </ul>"""
        add_content_type(type="news", user="fangiot", layout=layout, selector="#newslist")
        add_content(type="news", user="fangiot", content="I am happy")
        add_content(type="news", user="fangiot", content="Woaw, wonderful day!")

        cms_page = add_cms_contain("fangiot", page)
        assert_that(cms_page, is_html_equal(expected_page))

class HTMLMatcher(BaseMatcher):

    def __init__(self, html):
        self.html = self.strip_all(html)

    def strip_all(self, string):
        return re.sub("\s", "", string)

    def _matches(self, item):
        return self.strip_all(item) == self.html

is_html_equal = HTMLMatcher
