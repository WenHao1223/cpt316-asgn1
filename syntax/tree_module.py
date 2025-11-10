# Define PARSE_NODE_TYPE for node types
PARSE_NODE_TYPE = [
    '<statement>',
    '<expression>',
    '<term>',
    '<factor>',
    
    'identifier',
    'number',
    'operator',
    'assignment',
    'parenthesis',
    'statement_terminator',
]

class ParseTree:
    def __init__(self, node_type, value=None, children=None):
        self.node_type = node_type
        self.value = value
        self.children = children if children else []

        # Validate the node type
        if not isinstance(node_type, str):
            raise ValueError(f"Invalid node type: {type(node_type)}")
        
        # Allow value to be str, int, float, or None (not just list)
        if value is not None and not isinstance(value, (str, int, float)):
            raise ValueError(f"Invalid value type: {type(value)}")
        
        # Validate the children
        if not isinstance(self.children, list):
            raise ValueError(f"Invalid children type: {type(self.children)}")
        
        # Validate the node value
        if node_type not in PARSE_NODE_TYPE:
            raise ValueError(f"Invalid node value: {node_type}")
        
    def __repr__(self):
        return f"ParseTree(node_type={self.node_type}, value={self.value}, children={self.children})"
    
    # To print the tree in a readable format
    def __str__(self, prefix="", is_last=True, is_root=True):
        display_value = f": {self.value}" if self.value is not None else ""
        if is_root:
            line = f"{self.node_type}{display_value}\n"
        else:
            connector = "└── " if is_last else "├── "
            line = f"{prefix}{connector}{self.node_type}{display_value}\n"
        new_prefix = prefix + ("    " if is_last else "│   ")
        for i, child in enumerate(self.children):
            child_is_last = (i == len(self.children) - 1)
            line += child.__str__(new_prefix, child_is_last, False)
        return line
    

def parse_tree_to_syntax_tree(parse_tree):
    def build_expr(node):
        # Handles <expression>, <term>, <factor>
        if node.node_type in ("<expression>", "<term>"):
            children = node.children
            if len(children) == 1:
                return build_expr(children[0])
            else:
                # Operator is always at odd indices
                op = None
                operands = []
                i = 0
                while i < len(children):
                    if i % 2 == 0:
                        operands.append(build_expr(children[i]))
                    else:
                        op = children[i].value
                    i += 1
                # Build tree from right to left for correct precedence
                tree = operands[-1]
                for j in range(len(operands) - 2, -1, -1):
                    tree = ParseTree("operator", op, [operands[j], tree])
                return tree
        elif node.node_type == "<factor>":
            # Only one child: number, identifier, or parenthesis
            child = node.children[0]
            if child.node_type == "parenthesis":
                # Parenthesis: child[1] is the expression
                return build_expr(node.children[1])
            elif child.node_type == "number":
                return ParseTree("number", child.value, [])
            elif child.node_type == "identifier":
                return ParseTree("identifier", child.value, [])
            else:
                return None
        elif node.node_type in ("number", "identifier"):
            return ParseTree(node.node_type, node.value, [])
        else:
            return None

    if parse_tree.node_type == "<statement>":
        identifier = None
        expr = None
        for child in parse_tree.children:
            if child.node_type == "identifier":
                identifier = ParseTree("identifier", child.value, [])
            elif child.node_type == "<expression>":
                expr = build_expr(child)
        return ParseTree("assignment", "=", [identifier, expr])
    else:
        raise ValueError("Only <statement> parse trees are supported.")