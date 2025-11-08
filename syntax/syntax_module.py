from lexer.lexer_module import Lexer, PATTERN, Token

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
        if not self.match(expected_type, expected_lexeme):
            if self.current_token is None and expected_lexeme == ';' and expected_type == 'STATEMENT_TERMINATOR':
                print(f"SyntaxError at end of input: "
                    f"Unexpected end of input: Missing '{expected_lexeme}'")
                return False
            elif self.current_token is None:
                print(f"SyntaxError at end of input: "
                f"Expected '{expected_lexeme}'")
                return False
            else:
                print(f"SyntaxError at position {self.current_token.pos}: "
                f"Expected '{expected_lexeme}' "
                f"before '{self.current_token.lexeme}'")
                return False
        self.get_next_token()
        return True

    # <statement> -> <identifier> = <expression> ;
    def parse_statement(self) -> bool:
        if not self.expect('IDENTIFIER'):
            return False
        if not self.expect('ASSIGNMENT', '='):
            return False
        if not self.parse_expression():
            return False
        if not self.expect('STATEMENT_TERMINATOR', ';'):
            return False
        return True

    # <expression> -> <term> | <expression> + <term> | <expression> - <term>
    def parse_expression(self) -> bool:
        if not self.parse_term():
            return False
        while self.match('OPERATOR', '+') or self.match('OPERATOR', '-'):
            self.get_next_token()
            if not self.parse_term():
                return False
        return True

    # <term> -> <factor> | <term> * <factor> | <term> / <factor>
    def parse_term(self) -> bool:
        if not self.parse_factor():
            return False
        while self.match('OPERATOR', '*') or self.match('OPERATOR', '/'):
            self.get_next_token()
            if not self.parse_factor():
                return False
        return True

    # <factor> -> <integer> | <identifier> | ( <expression> )
    def parse_factor(self) -> bool:
        if self.match('NUMBER'):
            self.get_next_token()
            return True
        elif self.match('IDENTIFIER'):
            self.get_next_token()
            return True
        elif self.match('PARENTHESIS', '('):
            self.get_next_token()
            if not self.parse_expression():
                return False
            if not self.expect('PARENTHESIS', ')'):
                return False
            return True
        else:
            if self.current_token is not None:
                print(f"SyntaxError at position {self.current_token.pos}: "
                    f"Unexpected token {self.current_token.type} ('{self.current_token.lexeme}') in factor")
            else:
                print(f"SyntaxError at end of input: Unexpected end of input in factor")
            self.get_next_token()
            return False

    def parse(self) -> bool:
        return self.parse_statement()