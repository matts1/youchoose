class Node(object):
    def __init__(self, text, parent):
        self.label = str(type(self)).split(".")[1]
        self.text = text
        self.parent = parent
        self.block = False

    def eval(self, context):
        raise NotImplementedError

    def __repr__(self):
        return "{} ({})".format(self.label, self.text)
