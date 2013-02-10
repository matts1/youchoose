from .node import Node

class TextNode(Node):
    def __repr__(self):
        if len(self.text) <= 40:
            return '"{}"'.format(self.text)
        return '"{}...{}"'.format(self.text[:20], self.text[-20:])

    def eval(self, context):
        return self.text
