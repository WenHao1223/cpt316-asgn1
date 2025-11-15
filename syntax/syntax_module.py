from lexer.lexer_module import Lexer
from .tree_module import ParseTree, parse_tree_to_syntax_tree
from .export_tree_module import export_tree_png, clear_export_folder

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
        if not self.expect("IDENTIFIER"):
            return None
        id_token = self.current_token
        if not self.expect("ASSIGNMENT", "="):
            return None
        expr_tree = self.parse_expression()
        if not expr_tree:
            return None
        if not self.expect("STATEMENT_TERMINATOR", ";"):
            return None
        print("Statement parsed successfully.\n")
        return ParseTree("<statement>", None, [
            ParseTree("identifier", id_token.lexeme),
            ParseTree("assignment", "="),
            expr_tree,
            ParseTree("statement_terminator", ";"),
        ])

    # Parse <expression>
    def parse_expression(self, left_expr=None):
        print("Parsing <expression>...")

        if left_expr is None:
            left_term = self.parse_term()
            if not left_term:
                return None
            left_expr = ParseTree("<expression>", None, [left_term])

        if self.match("OPERATOR", "+") or self.match("OPERATOR", "-"):
            op_token = self.current_token
            self.get_next_token()

            right_term = self.parse_term()
            if not right_term:
                return None
            new_expr = ParseTree("<expression>", None, [
                left_expr,
                ParseTree("operator", op_token.lexeme),
                right_term
            ])
            return self.parse_expression(new_expr)
        return left_expr

    # Parse <term>
    def parse_term(self, left_term=None):
        print("Parsing <term>...")

        if left_term is None:
            left_factor = self.parse_factor()
            if not left_factor:
                return None
            left_term = ParseTree("<term>", None, [left_factor])

        if self.match("OPERATOR", "*") or self.match("OPERATOR", "/"):
            op_token = self.current_token
            self.get_next_token()

            right_factor = self.parse_factor()
            if not right_factor:
                return None

            new_term = ParseTree("<term>", None, [
                left_term,
                ParseTree("operator", op_token.lexeme),
                right_factor
            ])
            return self.parse_term(new_term)
        return left_term

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
            if not self.expect("PARENTHESIS", ")"):
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
    
    def parse_all_statements(self):
        def process_statement(tokens):
            statement_source = ' '.join(t.lexeme for t in tokens)
            print(f'Processing statement "{statement_source}"...')
            temp_lexer = type(self.lexer)("")
            temp_lexer.tokens = tokens.copy()
            temp_lexer.invalids = []
            parser = Syntax(temp_lexer)
            return parser.parse_statement()

        statements = []
        statement_tokens = []
        for token in self.tokens:
            statement_tokens.append(token)
            if token.type == "STATEMENT_TERMINATOR" and token.lexeme == ";":
                parse_tree = process_statement(statement_tokens)
                statements.append(parse_tree)
                statement_tokens = []
        # After loop, check for leftover tokens (missing semicolon)
        if statement_tokens:
            parse_tree = process_statement(statement_tokens)
            statements.append(parse_tree)
        return statements
    
    # Main parse function
    def parse(self):
        # Parse all statements and export each parse tree as line-N-parse-tree.png
        all_parse_trees = self.parse_all_statements()
        results = []
        clear_export_folder()
        for idx, parse_tree in enumerate(all_parse_trees):
            if parse_tree:
                # Export syntax tree as line-N-syntax-tree.png
                syntax_tree = parse_tree_to_syntax_tree(parse_tree)
                print(f"\nSyntax Tree (line {idx}):")
                print(syntax_tree)
                export_tree_png(syntax_tree, f"output/line-{idx}-syntax-tree.png")

                # Export parse tree as line-N-parse-tree.png
                print(f"\nParse Tree (line {idx}):")
                print(parse_tree)
                export_tree_png(parse_tree, f"output/line-{idx}-parse-tree.png")

                results.append((syntax_tree, parse_tree))
            else:
                print(f"Parsing failed for statement at line {idx}.")
                results.append((None, None))
        return results