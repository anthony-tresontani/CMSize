import requests

SERVER = "localhost"
PORT = 8888
USER = "jojo"
url = "http://%(server)s:%(port)d/cms/%(user)s/" % {"server":SERVER, "port":PORT, "user":USER}

html = """<html>
              <body>
                  <div id="news"></div>
              </body>
          </html>
"""
payload = {"dom":html}
response = requests.post(url, data=payload)

print response.content
