class Node:
    def __init__(self, label: str, value: str = None, children=None):
        self.label = label
        self.value = value
        self.children = []
        if children:
            for c in children:
                if c is not None:
                    self.children.append(c)

    def add_child(self, child):
        if child is not None:
            self.children.append(child)
        return child

    def text(self):
        return f"{self.label}: {self.value}" if self.value is not None else self.label

def print_tree(root):
    def _walk(node, prefix: str = "", is_last: bool = True):
        if node is None:
            print(f"{prefix}|__ <None>")
            return
        connector = "|__ "
        print(f"{prefix}{connector}{node.text()}")
        child_prefix = prefix + ("    " if is_last else "|   ")
        real_children = [c for c in node.children if c is not None]
        for i, ch in enumerate(real_children):
            _walk(ch, child_prefix, i == len(real_children) - 1)
    _walk(root)