from .evalnode import EvalNode
from .groupnode import GroupNode, BlockNode
from .textnode import TextNode
from .fornode import ForNode
from .ifnode import IfNode, ElifNode, ElseNode
from .runnode import RunNode

import re
from functions.template import makecontext
TEMPLATE_DIR = __file__[::-1].split("/", 2)[2][::-1] + "/templates/"

def render(filename, response, context=None):
    context = makecontext(context, response)
    result = Parser(filename).parse().eval(context)
    if response != None:
        response.write(result)
    else:
        return result

class Parser(object):
    def __init__(self, data, isfile=True):
        self.commands = {
                "include": IncludeNode,
                "for": ForNode,
                "if": IfNode,
                "elif": ElifNode,
                "else": ElseNode,
                "run": RunNode,
        }
        self.filename = ""
        if isfile:
            self.filename = TEMPLATE_DIR + data
            #print(self.filename)
            try:
                self.text = open(TEMPLATE_DIR + data).read()
            except IOError:
                raise IOError("Couldn't find file " + data)
        else:
            self.text = data
        self.text = re.sub("[\t \n]+", " ", self.text, flags=re.M) + "{##}"
        # {##} adds a comment at the end, so that it renders the last bit
        self.upto = 0

        self.endtags = {
            "{": "}",
            "%": "%",
            "#": "#",
        }
        self.opentags = set(self.endtags)
        self.root = GroupNode()

    def parse(self, parent=None, first=True):
        if parent == None:
            parent = self.root
        last = False
        start = self.upto
        if first: start = -1
        while self.upto < len(self.text):
            char = self.text[self.upto]
            if last and char in self.opentags:

                #start a tag
#                print(start, max(self.upto - 2, 0))
                parent.add_child(TextNode(self.text[start+1:max(self.upto - 1, 0)], parent))
                parent = self.find(self.endtags[char], parent)
                start = self.upto
                last = False


            if not last and char == "{":
                last = True
            else:
                last = False
            self.upto += 1
        if parent.parent != None:
            #still inside a block
            pass #raise SyntaxError("{} block has not been closed".format(parent.label))
        return parent

    def find(self, end, parent):
        self.upto += 1 #leave the opening tag
        try:
            closeindex = self.text.index(end + "}", self.upto)
            inside = self.text[self.upto:closeindex].strip(" ")
            self.upto = closeindex + 1
            if end == "}":
                #self.upto += 1
                parent.add_child(EvalNode(inside, parent))
            elif end == "%":
                inside = inside.split(" ", 1)
                if len(inside) == 1:
                    cmd = inside[0]
                    args = ""
                else:
                    cmd = inside[0]
                    args = inside[1]
                if cmd in self.commands:
                    if cmd == "include":
                        node = self.commands[cmd](args, parent, self.filename)
                    else:
                        node = self.commands[cmd](args, parent)
                    parent = node.parent #allows node to change the parent. Lets elif / else change the parent
                    parent.add_child(node)
                    #if "footer" in args:
                    #    print(self.root.children)
                    if node.block:
                            self.parse(node, False)
                elif cmd == "end": #special command
                    if args not in self.commands:
                        raise SyntaxError("Command {} cannot be ended, as it does not exist".format(args))
                    if not isinstance(parent, self.commands[args]):
                        raise SyntaxError("Cannot end command {}, in block {}".format(args, parent.label))
                    parent = parent.parent
                else:
                    raise SyntaxError("{} is not a valid command ({{% {} %}})".format(cmd, " ".join(inside)))
        except ValueError:
            raise SyntaxError("{}}} never appeared after opening tag".format(end))
#        if end == "%":
#            print(closeindex, self.upto, self.text)
#            print(cmd, args, '"{}"'.format(self.text[closeindex + 2]), closeindex)
        return parent

#NEEDS TO BE IN SAME FILE TO GET THE SAME TEMPLATE DIR
class IncludeNode(BlockNode):
    def __init__(self, args, parent, directory):
        directory = ("/".join(directory.split("/")[:-1]) + "/")[len(TEMPLATE_DIR):]
        super(IncludeNode, self).__init__(args, parent)
        if args[0] == "/":
           args = args[1:] #strips / off start
        else:
            #relative
            args =  directory + args
        for child in Parser(args).parse().children:
            self.add_child(child)
        self.block = False

if __name__ == "__main__":
    tree = Parser("register.html").parse()

    print(tree)
    print(tree.eval({'firstname': 'matt', 'lastname': 'stark'}))

