from lexer.lexer_module import Lexer, PATTERN
from syntax.node_module import Node
# <statement> -> <identifier> = <expression> ;
# <expression> -> <term> | <expression> + <term> | <expression> - <term>
# <term> -> <factor> | <term> * <factor> | <term> / <factor>
# <factor> -> <integer> | <identifier> | ( <expression> )

class Syntax:

    def __init__(self, lexer: Lexer):
        self.lexer = lexer
        # Check any invalid tokens before parsing
        if lexer.invalids:
            raise ValueError("Cannot parse input with lexical errors.")
        self.tokens = lexer.tokens
        self.current_index = 0 
        self.current_token = None
        self.get_next_token()

    def get_next_token(self):
        if self.current_index < len(self.tokens):
            self.current_token = self.tokens[self.current_index]
            # print(f"Current token: {self.current_token.type} ('{self.current_token.lexeme}') at position {self.current_token.pos}")
            self.current_index += 1
        else: self.current_token = None
    
    def match(self, expected_type: str, expected_lexeme: str = None) -> bool:
        if self.current_token is None:
            return False
        if self.current_token.type != expected_type:
            return False
        if expected_lexeme is not None and self.current_token.lexeme != expected_lexeme:
            return False
        return True
    
    def expect(self, expected_type: str, expected_lexeme: str = None) -> bool:
        if self.match(expected_type, expected_lexeme):
            self.get_next_token()
            return True
        else:
            if self.current_token is None:
                exp = f"'{expected_lexeme}'" if expected_lexeme else expected_type
                print(f"SyntaxError at end of input: expected {exp} before end of input")
            else:
                if expected_type == "STATEMENT_TERMINATOR" and expected_lexeme == ";":
                    print(f"SyntaxError at position {self.current_token.pos}: unexpected '{self.current_token.lexeme}'")
                else:
                    exp = f"'{expected_lexeme}'" if expected_lexeme else expected_type
                    print(f"SyntaxError at position {self.current_token.pos}: "
                            f"expected {exp} before '{self.current_token.lexeme}'")
            return False
        
    def parse_statement(self) -> Node:
        print("Parsing <statement>...")
        # Build the parse tree node for statement
        node = Node("<statement>")

        # id
        token_id = self.expect("IDENTIFIER")
        node.add_child(Node("id", self.lexer.tokens[self.current_index - 1].lexeme))
        
        # assignment '='
        token_assign = self.expect("ASSIGNMENT", "=")
        node.add_child(Node("assignment", self.lexer.tokens[self.current_index - 1].lexeme))
        
        # <expression>
        expr_node = self.parse_expression()
        node.add_child(expr_node)
        
        # statement terminator ';'
        token_term = self.expect("STATEMENT_TERMINATOR", ";")
        node.add_child(Node("statement_terminator", self.lexer.tokens[self.current_index - 1].lexeme))
        return node

    def parse_expression(self) -> Node:
        left = self.parse_term()
        while self.match("OPERATOR", "+") or self.match("OPERATOR", "-"):
            op_token = self.current_token
            self.get_next_token()
            right = self.parse_term()
            new_left = Node("<expression>")
            new_left.add_child(self._wrap_as("<term>", left))
            new_left.add_child(Node("OPERATOR", op_token.lexeme))
            new_left.add_child(self._wrap_as("<term>", right))
            left = new_left
        if left.label != "<expression>":
            expr_node = Node("<expression>")
            expr_node.add_child(self._wrap_as("<term>", left))
            return expr_node

    def parse_term(self) -> Node:
        left = self.parse_factor()
        while self.match("OPERATOR", "*") or self.match("OPERATOR", "/"):
            op_token = self.current_token
            self.get_next_token()
            right = self.parse_factor()
            new_left = Node("<term>")
            new_left.add_child(self._wrap_as("<factor>", left))
            new_left.add_child(Node("OPERATOR", op_token.lexeme))
            new_left.add_child(self._wrap_as("<factor>", right))
            left = new_left

        if left.label != "<term>":
            term_node = Node("<term>")
            term_node.add_child(self._wrap_as("<factor>", left))
            return term_node
        return left

    def parse_factor(self) -> Node:
        if self.match("NUMBER"):
            node = Node("<factor>")
            node.add_child(Node("NUMBER", self.current_token.lexeme))
            self.get_next_token()
            return node
        elif self.match("IDENTIFIER"):
            node = Node("<factor>")
            node.add_child(Node("IDENTIFIER", self.current_token.lexeme))
            self.get_next_token()
            return node
        elif self.match("PARENTHESIS", "("):
            node = Node("<factor>")
            node.add_child(Node("PARENTHESIS", self.current_token.lexeme))
            self.get_next_token()
            expr_node = self.parse_expression()
            node.add_child(expr_node)
            if not self.expect("PARENTHESIS", ")"):
                return None
            node.add_child(Node("PARENTHESIS", self.lexer.tokens[self.current_index - 1].lexeme))
            return node
        else:
            if self.current_token is None:
                print("SyntaxError at end of input: expected NUMBER, IDENTIFIER, or '('.")
            else:
                if self.current_token.type == "PARENTHESIS" and self.current_token.lexeme == ")":
                    print(f"SyntaxError at position {self.current_token.pos}: unexpected ')'")
                else:
                    print(f"SyntaxError at position {self.current_token.pos}: expected NUMBER, "
                            f"IDENTIFIER, or '(', found '{self.current_token.lexeme}'")
            return None
    
    def parse(self) -> bool:
        return self.parse_statement()
    
    def _wrap_as(self, label: str, node: Node) -> Node:
        if node.label == label:
            return node
        wrap = Node(label)
        wrap.add_child(node)
        return wrap