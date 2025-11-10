# To run this file directly
# python main.py

# To test the lexer module
# python -m lexer.__init__

from lexer.lexer_module import Lexer
from lexer import lexer_error_handling, print_token_stream, print_invalids, print_counts
from syntax.syntax_module import Syntax

# Main program
if __name__ == "__main__":
    # Get input line from user
    line = str(input("Enter a line of code to lex: "))
    # line = "x = (y + 3) * 2;"

    lexer = Lexer(line)
    tokens, invalids, counts = lexer.lex()

    print(f"\nInput: {line}\n")

    # # Lexical error handling
    lexer_error_handling(invalids)

    # # # Print results
    print_token_stream(tokens)
    print_invalids(invalids)
    print_counts(counts)

    parser = Syntax(lexer)
    tree = parser.parse()