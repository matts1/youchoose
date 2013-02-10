from .node import Node

class RunNode(Node):
    def eval(self, context):
        exec(self.text, {}, context)
        return "" #should not return anything, but needs to return string
