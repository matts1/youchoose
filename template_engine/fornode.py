from .groupnode import BlockNode

class ForNode(BlockNode):
    def __init__(self, args, parent):
        super(ForNode, self).__init__(args, parent)
        args = args.split(" in ", 1)
        if len(args) != 2:
            raise SyntaxError("for loop contains no in")
        self.varname, self.iterable = args

    def eval(self, context):
        output = ""
        try:
            iterable = eval(self.iterable, {}, context)
        except NameError as e:
            return "{{% {}: {} %}}".format(self.args, e)
        for item in eval(self.iterable, {}, context):
            context[self.varname] = item
            output += self.eval_children(context)
        return output
