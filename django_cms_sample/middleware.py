from django.conf import settings
import requests
from requests.packages.urllib3.connectionpool import HTTPConnectionPool


url = "http://%(server)s:%(port)d/cms/%(user)s/" % {"server": settings.CMS_SERVER,
                                                    "port": settings.CMS_PORT,
                                                    "user": settings.CMS_USER}

class CMSMiddleware(object):
    def process_response(self, request, response):
        try:
            html = requests.post(url, data={"dom":response.content})
            response.content = html.content
        except HTTPConnectionPool, e:
            print e
        finally:
            return response