from lexer.lexer_module import Lexer, PATTERN

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
            return False
        if not self.expect("ASSIGNMENT", "="):
            return False
        if not self.parse_expression():
            return False
        if not self.expect("STATEMENT_TERMINATOR", ";"):
            return False
        print("Statement parsed successfully.")
        return True

    # Parse <expression>
    def parse_expression(self) -> bool:
        print("Parsing <expression>...")
        if not self.parse_term():
            return False
        # Then check for + or - and recurse
        while(self.match("OPERATOR", "+") or self.match("OPERATOR", "-")):
            self.get_next_token()
            if not self.parse_term():
                return False
        return True

    # Parse <term>
    def parse_term(self) -> bool:
        print("Parsing <term>...")
        if not self.parse_factor():
            return False
        # Then check for * or / and recurse
        while(self.match("OPERATOR", "*") or self.match("OPERATOR", "/")):
            self.get_next_token()
            if not self.parse_factor():
                return False
        return True

    # Parse <factor>
    def parse_factor(self) -> bool:
        print("Parsing <factor>...")
        if self.match("NUMBER"):
            self.get_next_token()
            return True
        elif self.match("IDENTIFIER"):
            self.get_next_token()
            return True
        elif self.match("PARENTHESIS", "("):
            self.get_next_token()
            if not self.parse_expression():
                return False
            if not self.expect("PARENTHESIS", ")"):
                return False
            return True
        else:
            if self.current_token is None:
                print("SyntaxError at end of input: expected NUMBER, IDENTIFIER, or '('.")
            else:
                if self.current_token.type == "PARENTHESIS" and self.current_token.lexeme == ")":
                    print(f"SyntaxError at position {self.current_token.pos}: unexpected ')'")
                else:
                    print(f"SyntaxError at position {self.current_token.pos}: expected NUMBER, "
                            f"IDENTIFIER, or '(', found '{self.current_token.lexeme}'")
            return False
    
    # Main parse function
    def parse(self) -> bool:
        return self.parse_statement()