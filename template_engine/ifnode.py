from .groupnode import BlockNode

class IfNode(BlockNode):
    def __init__(self, args, parent):
        super(IfNode, self).__init__(args, parent)
        self.next = None
        self.prev = None
        self.allowed = True

    def eval(self, context):
        if self.allowed:
            try:
                if eval(self.args, {}, context):
                    if self.next:
                        self.next.allowed = False
                    self.allowed = True
                    return self.eval_children(context)
            except NameError as e:
                return "{{% {}: {} %}}".format(self.args, e)
        else:
            if self.next:
                self.next.allowed = False
        self.allowed = True
        return ""


class ElifNode(IfNode):
    def __init__(self, args, parent):
        super(ElifNode, self).__init__(args, parent)
        if not ("ElifNode" in str(type(parent)) or "IfNode" in str(type(parent))):
            raise SyntaxError("{} needs to follow either an if or an elif".format(self.label[:4]))
        self.prev = self.parent
        self.parent.next = self
        self.parent = self.parent.parent

class ElseNode(ElifNode):
    def __init__(self, args, parent):
        super(ElseNode, self).__init__("True", parent)
