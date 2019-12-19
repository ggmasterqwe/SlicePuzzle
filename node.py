class Node:

    def __init__(self, value, parent=None):
        self.children = []
        self.seen = False
        self.next_node = None
        self.value = value
        self.parent = parent

    def get_parent(self):
        return self.parent

    def get_value(self):
        return self.value

    def add_children(self, child):
        self.children.append(child)


def rout(node):
    order = []
    while(True):
        if node.parent is not None:
            node = node.parent
        else:
            break
    while(True):
        order.append(node.value)
        for child in node.children:
            if child.seen is True:
                node = child
        if (True in [x.seen for x in node.children]) is False:
            break
    return order


def show_order(order):
    for node in order:
        print('', node[0], '\n', node[1], '\n', node[2], '\n')
