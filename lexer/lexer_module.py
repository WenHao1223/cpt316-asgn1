from .token_module import Token
import re

PATTERN = {
    'IDENTIFIER': r'[A-Za-z_][A-Za-z0-9_]*',
    'NUMBER': r'\d+(?:\.\d+)?',
    'SINGLE': {
        'OPERATOR': r'[\+\-\*\/]',
        'ASSIGNMENT': r'=',
        'PARENTHESIS': r'[\(\)]',
        'STATEMENT_TERMINATOR': r';',
    }
}

# Pre-compile regexes for speed and correctness
IDENT_RE = re.compile(PATTERN['IDENTIFIER'])
NUMBER_RE = re.compile(PATTERN['NUMBER'])
SINGLE_RE = {k: re.compile(v) for k, v in PATTERN['SINGLE'].items()}

class Lexer:
    def __init__(self, source: str):
        self.source = source # Input source code as a string
        self.position = 0
        self.length = len(source)
        self.tokens: list[Token] = []  # List of tokens
        self.invalids: list[tuple[int, str]] = []  # List of tuples (position, character)

    # Skip whitespace characters
    def skip_whitespace(self):
        while self.position < self.length and self.source[self.position].isspace():
            self.position += 1

    # Scan identifiers
    def scan_identifier(self):
        start = self.position
        while (self.position < self.length and 
            IDENT_RE.match(self.source, self.position)):
            self.position += 1
        lexeme = self.source[start:self.position]
        self.tokens.append(Token('IDENTIFIER', lexeme, start))

    # Scan numbers
    def scan_number(self):
        start = self.position
        while (self.position < self.length and 
            NUMBER_RE.match(self.source, self.position)):
            self.position += 1
        lexeme = self.source[start:self.position]
        self.tokens.append(Token('NUMBER', lexeme, start))

    # Scan single character tokens
    def scan_single(self):
        start = self.position
        char = self.source[self.position]

        # Scan operators, assignments, parentheses, and statement terminators
        for token_type, pattern in SINGLE_RE.items():
            if pattern.match(char):
                self.tokens.append(Token(token_type, char, start))
                break
        else:
            # If no match, it's an invalid character
            self.invalids.append((start, char))

        self.position += 1

    # Main lexing function
    def lex(self) -> tuple[list[Token], list[tuple[int, str]], dict[str, int]]:
        """Returns a tuple of (tokens, invalids, counts_by_type)
        - tokens: list of Token
        - invalids: list of (pos, char)
        - counts_by_type: dict with per-type counts + 'TOTAL'
        """

        # Lexing loop
        while self.position < self.length:
            self.skip_whitespace()
            # Check for end of input
            if self.position >= self.length:
                break

            # Get the current character
            current_char = self.source[self.position]

            # Determine the type of token to scan
            if re.match(PATTERN['IDENTIFIER'], current_char):
                self.scan_identifier()
            elif re.match(PATTERN['NUMBER'], current_char):
                self.scan_number()
            else:
                # Match against single character token patterns
                # including operators, assignments, parentheses, and statement terminators
                # If no match, it's a single character token
                self.scan_single()

        # Count tokens by type
        counts_by_type: dict[str, int] = {}
        for token in self.tokens:
            counts_by_type[token.type] = counts_by_type.get(token.type, 0) + 1

        # Add summary counts
        counts_by_type['TOTAL'] = len(self.tokens)
        counts_by_type['INVALID'] = len(self.invalids)

        return self.tokens, self.invalids, counts_by_type
