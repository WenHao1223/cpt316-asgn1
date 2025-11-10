from lexer.lexer_module import Lexer
from .tree_module import ParseTree, parse_tree_to_syntax_tree
from .export_tree_module import export_tree_png

# Grammar Rules:
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

    # Helper function to advance to the next token
    def get_next_token(self):
        if self.current_index < len(self.tokens):
            self.current_token = self.tokens[self.current_index]
            self.current_index += 1
        else: self.current_token = None
    
    # Helper function to check if the current token matches expected type and lexeme
    def match(self, expected_type: str, expected_lexeme: str = None) -> bool:
        if self.current_token is None:
            return False
        if self.current_token.type != expected_type:
            return False
        if expected_lexeme is not None and self.current_token.lexeme != expected_lexeme:
            return False
        return True
    
    # Helper function to expect a token of a certain type and lexeme, advancing if matched
    def expect(self, expected_type: str, expected_lexeme: str = None) -> bool:
        if self.match(expected_type, expected_lexeme):
            self.get_next_token()
            return True
        else:
            if self.current_token is None:
                exp = f"'{expected_lexeme}'" if expected_lexeme else expected_type
                print(f"SyntaxError at end of input: expected {exp} before end of input")
            elif expected_type == "STATEMENT_TERMINATOR" and expected_lexeme == ";":
                print(f"SyntaxError at position {self.current_token.pos}: "
                    f"unexpected token '{self.current_token.lexeme}'")
            else:
                exp = f"'{expected_lexeme}'" if expected_lexeme else expected_type
                print(f"SyntaxError at position {self.current_token.pos}: "
                        f"expected {exp} before '{self.current_token.lexeme}'")
            return False
    
    # Parse <statement>
    def parse_statement(self) -> bool:
        print("Parsing <statement>...")
        if not self.match("IDENTIFIER"):
            return None
        id_token = self.current_token
        self.get_next_token()
        if not self.expect("ASSIGNMENT", "="):
            return None
        expr_tree = self.parse_expression()
        if not expr_tree:
            return None
        if not self.expect("STATEMENT_TERMINATOR", ";"):
            return None
        print("Statement parsed successfully.")
        return ParseTree("<statement>", None, [
            ParseTree("identifier", id_token.lexeme),
            ParseTree("assignment", "="),
            expr_tree,
            ParseTree("statement_terminator", ";"),
        ])

    # Parse <expression>
    def parse_expression(self) -> bool:
        print("Parsing <expression>...")
        term_tree = self.parse_term()
        if not term_tree:
            return None
        children = [term_tree]
        while self.match("OPERATOR", "+") or self.match("OPERATOR", "-"):
            op_token = self.current_token
            self.get_next_token()
            next_term = self.parse_term()
            if not next_term:
                return None
            children.append(ParseTree("operator", op_token.lexeme))
            children.append(next_term)
        return ParseTree("<expression>", None, children)

    # Parse <term>
    def parse_term(self) -> bool:
        print("Parsing <term>...")
        factor_tree = self.parse_factor()
        if not factor_tree:
            return None
        children = [factor_tree]
        while self.match("OPERATOR", "*") or self.match("OPERATOR", "/"):
            op_token = self.current_token
            self.get_next_token()
            next_factor = self.parse_factor()
            if not next_factor:
                return None
            children.append(ParseTree("operator", op_token.lexeme))
            children.append(next_factor)
        return ParseTree("<term>", None, children)

    # Parse <factor>
    def parse_factor(self) -> bool:
        print("Parsing <factor>...")
        node = None
        if self.match("NUMBER"):
            num_token = self.current_token
            self.get_next_token()
            return ParseTree("<factor>", None, [ParseTree("number", num_token.lexeme)])
        elif self.match("IDENTIFIER"):
            id_token = self.current_token
            self.get_next_token()
            return ParseTree("<factor>", None, [ParseTree("identifier", id_token.lexeme)])
        elif self.match("PARENTHESIS", "("):
            left_paren_token = self.current_token
            self.get_next_token()
            expr_tree = self.parse_expression()
            if not expr_tree:
                return None
            if not self.match("PARENTHESIS", ")"):
                return None
            right_paren_token = self.current_token
            self.get_next_token()
            node = ParseTree("<factor>", None, [
                ParseTree("parenthesis", left_paren_token.lexeme),
                expr_tree,
                ParseTree("parenthesis", right_paren_token.lexeme)
            ])
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
    
    # Main parse function
    def parse(self) -> bool:
        parseTree = self.parse_statement()
        syntaxTree = parse_tree_to_syntax_tree(parseTree) if parseTree else None

        if syntaxTree and parseTree:
        # if parseTree:
            print("\nSyntax Tree:")
            print(syntaxTree)
            export_tree_png(syntaxTree, "output/syntax_tree.png")

            print("\nParse Tree:")
            print(parseTree)
            export_tree_png(parseTree, "output/parse_tree.png")

            return syntaxTree, parseTree
            # return parseTree
        else:
            print("Parsing failed due to syntax errors.")
            return None