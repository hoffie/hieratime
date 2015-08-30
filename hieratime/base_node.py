class BaseNode(object):
    parent = None

    def get_root(self):
        root = self
        while root.parent:
            root = root.parent
        return root
