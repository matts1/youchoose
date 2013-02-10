from .node import Node

class EvalNode(Node):
    def __repr__(self):
        return "EvalNode({})".format(self.text)

    def eval(self, context):
        try:
            result = str(eval(self.text, {}, context))
        except SyntaxError as e:
            raise e
        except Exception as e:
            result = '{{{{ {} : "{}" }}}}'.format(self.text, e)
        return result
