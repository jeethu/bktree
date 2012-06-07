class BKTree(object):
    def __init__(self, distance_fn, objs=None):
        self.distance_fn = distance_fn
        if objs is not None:
            it = iter(objs)
            root = it.next()
            self.tree = BKNode(root)
            for obj in it:
                self._add(self.tree, obj)
        else:
            self.tree = None

    def add(self, obj):
        if self.tree is None:
            self.tree = BKNode(obj)
        else:
            self._add(self.tree, obj)

    def _add(self, parent, obj):
        pobj = parent.obj
        d = self.distance_fn(obj, pobj)
        if d in parent:
            self._add(parent[d], obj)
        else:
            parent[d] = BKNode(obj)

    def search(self, obj, d):
        l = []
        if self.tree is not None:
            self._recursive_search(self.tree, l, obj, d)
        return sorted(l, key=lambda x: x[1])

    def _recursive_search(self, node, found, obj, d):
        current_distance = self.distance_fn(node.obj, obj)
        min_distance, max_distance = current_distance - d, current_distance + 1

        if current_distance <= d:
            found.append((node.obj, self.distance_fn(obj, node.obj)))

        for k in (x for x in node if x >= min_distance and x <= max_distance):
            self._recursive_search(node[k], found, obj, d)

    def render(self, filename=None):
        from graphviz import Digraph
        dot = Digraph()
        if self.tree is not None:
            dot.node(str(id(self.tree)), self.tree.obj)
            self._recursive_render(dot, str(id(self.tree)), self.tree)
        if filename is not None:
            dot.render(filename)
        return dot

    def _recursive_render(self, dot, parent, node):
        for key, child in node.items():
            dot.node(str(id(child)), child.obj)
            dot.edge(parent, str(id(child)), label='%d' % key)
            self._recursive_render(dot, str(id(child)), child)


class BKNode(dict):
    def __init__(self, obj):
        super(BKNode, self).__init__()
        self.obj = obj

    def __repr__(self):
        if len(self) == 0:
            return 'BKNode<%s>' % (repr(self.obj), )
        return 'BKNode<%s, %s>' % (repr(self.obj),
                                   super(BKNode, self).__repr__())
