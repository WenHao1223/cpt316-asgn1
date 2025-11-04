# Define TYPE_S for token types
TYPE_S = [
    'IDENTIFIER',
    'NUMBER',
    'OPERATOR',
    'ASSIGNMENT',
    'PARENTHESIS',
    'STATEMENT_TERMINATOR',
]

class Token:
    def __init__ (self, type_: str, lexeme: str, pos: int):
        self.type = type_
        self.lexeme = lexeme
        self.pos = pos

        # Validate the token type
        if not isinstance(type_, str):
            raise ValueError(f"Invalid token type: {type(type_)}")
        
        # Validate the lexeme
        if not isinstance(lexeme, str):
            raise ValueError(f"Invalid lexeme type: {type(lexeme)}")
        
        # Validate the position
        if not isinstance(pos, int):
            raise ValueError(f"Invalid position type: {type(pos)}")
        
        # Validate the token value
        if type_ not in TYPE_S:
            raise ValueError(f"Invalid token value: {type_}")
        
        # Validate the position value
        if pos < 0:
            raise ValueError(f"Invalid position value: {pos}")
    
    def __repr__(self):
        return f"Token(type={self.type}, lexeme='{self.lexeme}', pos={self.pos})"