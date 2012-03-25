from mongoengine import *

connect('cmsside')


class ContentType(Document):
    user = StringField(required=True)
    type = StringField(required=True)
    layout = StringField(required=True)
    selector = StringField(required=True)
    unique = BooleanField(default=False)

class Content(Document):
    user = StringField(required=True)
    content = StringField(required=True)
    type = StringField(required=True)
