# To run this file directly
# python main.py

# To test the lexer module
# python -m lexer.__init__

from lexer.lexer_module import Lexer
from lexer import print_token_stream, print_invalids, print_counts

# Main program
if __name__ == "__main__":
    # Get input line from user
    line = str(input("Enter a line of code to lex: "))

    lexer = Lexer(line)
    tokens, invalids, counts = lexer.lex()

    print(f"\nInput: {line}\n")
    print_token_stream(tokens)
    print_invalids(invalids)
    print_counts(counts)