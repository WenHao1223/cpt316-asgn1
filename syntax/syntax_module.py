import re
from lexer.lexer_module import PATTERN

IDENT_RE = re.compile(PATTERN['IDENTIFIER'])
NUMBER_RE = re.compile(PATTERN['NUMBER'])
EXPRESSION_OPERATION_RE = re.compile(r'[\+\-]')
TERM_OPERATION_RE = re.compile(r'[\*\/]')

class Syntax:
    def __init__(self, source: str):
        self.source = source
        self.position = 0
        self.length = len(source)

    # Skip whitespace characters
    def skip_whitespace(self):
        while self.position < self.length and self.source[self.position].isspace():
            self.position += 1

    # Report a syntax error with expected token and current position
    def syntax_error(self, expected: str):
        
        if self.position >= self.length:
            next_char = "end of input"
        else:
            next_char = f"'{self.source[self.position]}'"
        print(f"└── SyntaxError at position {self.position}: expected {expected} before {next_char}")

    # Parse a factor: identifier, number, or ( expression )
    def parse_factor(self) -> bool:
        if self.position >= self.length:
            self.syntax_error("factor")
            return False
        
        # Identifier
        m = IDENT_RE.match(self.source, self.position)
        if m:
            print(f"Factor: Identifier ({m.group(0)})")
            self.position += len(m.group(0))
            return True
        
        # Number
        m = NUMBER_RE.match(self.source, self.position)
        if m:
            print(f"Factor: Number ({m.group(0)})")
            self.position += len(m.group(0))
            return True
        
        # ( expression )
        if self.source[self.position] == '(':
            print("Factor: Left Parenthesis")
            self.position += 1
            self.skip_whitespace()
            
            if not self.parse_expression():
                return False
            
            self.skip_whitespace()
            if self.position < self.length and self.source[self.position] == ')':
                print("Factor: Right Parenthesis")
                self.position += 1
                return True
            else:
                self.syntax_error("')'")
                return False
        
        self.syntax_error("identifier, number, or '('")
        return False

    # Parse a term: factor followed by zero or more term operators
    def parse_term(self) -> bool:
        self.skip_whitespace()

        if not self.parse_factor():
            return False
        
        self.skip_whitespace()
        while self.position < self.length and TERM_OPERATION_RE.match(self.source, self.position):
            print(f"Term: Term Operator ({self.source[self.position]})")
            self.position += 1
            self.skip_whitespace()
            
            if not self.parse_factor():
                return False
            
            self.skip_whitespace()
        return True

    # Parse an expression: term followed by zero or more expression operators
    def parse_expression(self) -> bool:
        self.skip_whitespace()
        if not self.parse_term():
            return False
        
        self.skip_whitespace()
        while self.position < self.length and EXPRESSION_OPERATION_RE.match(self.source, self.position):
            print(f"Expression: Expression Operator ({self.source[self.position]})")
            self.position += 1
            self.skip_whitespace()
            
            if not self.parse_term():
                return False
            
            self.skip_whitespace()
        return True
    
    # Parse a statement: identifier = expression ;
    def parse_statement(self) -> bool:
        self.skip_whitespace()
        
        m = IDENT_RE.match(self.source, self.position)
        if not m:
            self.syntax_error("identifier")
            return False
        
        print(f"Statement: Identifier ({m.group(0)})")
        self.position += len(m.group(0))
        self.skip_whitespace()
        
        if self.position >= self.length or self.source[self.position] != '=':
            self.syntax_error("'='")
            return False
        
        print("Statement: Assignment Operator")
        self.position += 1
        self.skip_whitespace()
        
        if not self.parse_expression():
            return False
        
        self.skip_whitespace()
        if self.position >= self.length or self.source[self.position] != ';':
            self.syntax_error("';'")
            return False
        
        print("Statement: Statement Terminator")
        self.position += 1
        return True
    
    # Main parse function
    def parse(self) -> bool:
        """Parse the source code and return True if valid, False otherwise."""
        return self.parse_statement()