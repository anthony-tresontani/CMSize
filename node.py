CONTENT_ITEM = "<cms-content/>"
CONTENT_ITEMS_START = "<cms-items>"
CONTENT_ITEMS_END = "/<cms-items>"

class Node(object):
    def __str__(self):
        return self.content

class HTMLNode(Node):
    def __init__(self, content):
        self.content = content

class ContentNode(Node):
    def set_content(self, content):
        self.content = content

def tokenize_cms(string):
    tokens = []
    position = 0
    while len(string):
        next_element_index = string.find(CONTENT_ITEM)
        if next_element_index == 0:
            tokens.append(ContentNode())
            string = string[len(CONTENT_ITEM):]
        else:
            if next_element_index == -1:
                next_element_index = len(string)
            tokens.append(HTMLNode(string[:next_element_index]))
            string = string[next_element_index:]
    return tokens

def replace_content(string, content):
    tokens = tokenize_cms(string)
    content_tokens = filter(lambda token: isinstance(token, ContentNode), tokens)
    map(lambda content_token: content_token.set_content(content), content_tokens)
    return "".join(map(lambda token:str(token), tokens))

def replace_items(string, items):
    return string
