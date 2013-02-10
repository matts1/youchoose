from .node import Node

class GroupNode(Node):
    def __init__(self, parent=None):
        super(GroupNode, self).__init__("", parent)
        self.children = []
        self.block = True
        self.args = ""

    def add_child(self, child):
        child.parent = self
        self.children.append(child)

    def eval_children(self, context):
        results = [child.eval(context) for child in self.children]
#        print(self.label, results, "\nEND")
        return "".join(results)

    def eval(self, context={}):
        return self.eval_children(context)

    def __repr__(self):
        out = "\n".join(map(repr, self.children))
        return "{} ({}):\n  {}".format(self.label, self.args, "\n  ".join(out.split("\n")))

class BlockNode(GroupNode):
    def __init__(self, args, parent):
        super(BlockNode, self).__init__(parent)
        self.args = args
