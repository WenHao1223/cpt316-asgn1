from .lexer_module import Lexer

# Helper function for lexical error handling
def lexer_error_handling(invalids):
    if invalids:
        for pos, char in invalids:
            print(f"  LexicalError at position {pos}: invalid character '{char}'")
        print()

# Helper functions for printing results
def print_token_stream(tokens):
    print("Token Stream:")
    if tokens:
        print("  ┌────────────┬───────────────────────────┬─────────────────────┐")
        print("  │ Position   │ Token Type                │ Lexeme              │")
        print("  ├────────────┼───────────────────────────┼─────────────────────┤")
        for t in tokens:
            print(f"  │ {t.pos:<10} │ {t.type:<25} │ '{t.lexeme}'{(18-len(str(t.lexeme)))*' '}│")
        print("  └────────────┴───────────────────────────┴─────────────────────┘\n")
    else:
        print("  (empty)\n")

# Helper function to print invalid characters
def print_invalids(invalids):
    print("Invalid Characters:")
    if invalids:
        print("  ┌────────────┬─────────────────────┐")
        print("  │ Position   │ Invalid Character   │")
        print("  ├────────────┼─────────────────────┤")
        for pos, char in invalids:
            print(f"  │ {pos:<10} │ '{char}'{(18-len(str(char)))*' '}│")
        print("  └────────────┴─────────────────────┘\n")
    else:
        print("  (none)\n")

# Helper function to print token counts
def print_counts(counts):
    print("Token Counts:")
    print("  ┌───────────────────────────┬─────────┐")
    print("  │ Token Type                │ Count   │")
    print("  ├───────────────────────────┼─────────┤")
    for ttype, count in counts.items():
        if ttype not in ('TOTAL', 'INVALID'):
            print(f"  │ {ttype:<25} │ {count:<7} │")
    print("  ├───────────────────────────┼─────────┤")
    print(f"  │ {'TOTAL':<25} │ {counts.get('TOTAL', 0):<7} │")
    print(f"  │ {'INVALID':<25} │ {counts.get('INVALID', 0):<7} │")
    print("  └───────────────────────────┴─────────┘\n")

# Main program
if __name__ == "__main__":
    # Example input line
    line = "$x = (3 + 5) * 2;"
    print(f"Enter a line of code to lex: {line}")

    lexer = Lexer(line)
    tokens, invalids, counts = lexer.lex()

    print(f"\nInput: {line}\n")

    # Lexical error handling
    lexer_error_handling(invalids)

    # Print results
    print_token_stream(tokens)
    print_invalids(invalids)
    print_counts(counts)