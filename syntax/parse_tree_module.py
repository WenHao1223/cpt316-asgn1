# Define NODE_TYPE for node types
NODE_TYPE = [
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
        if node_type not in NODE_TYPE:
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