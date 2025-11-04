from .lexer_module import Lexer

# Helper functions for printing results
def print_token_stream(tokens):
    print("Token Stream:")
    for t in tokens:
        print(f"  [{t.pos}] {t.type:<7}  '{t.lexeme}'")
    if not tokens:
        print("  (empty)")
    print()

# Helper function to print invalid characters
def print_invalids(invalids):
    print("Invalid Characters:")
    for pos, char in invalids:
        print(f"  [{pos}] '{char}'")
    if not invalids:
        print("  (none)")
    print()

# Helper function to print token counts
def print_counts(counts):
    print("Token Counts:")
    for ttype, count in counts.items():
        print(f"  {ttype:<20} {count}")
    print(f"  {'TOTAL':<20} {counts['TOTAL']}")
    print(f"  {'INVALID':<20} {counts['INVALID']}")
    print()

# Main program
if __name__ == "__main__":
    # Example input line
    line = "x = (3 + 5) * 2;"

    lexer = Lexer(line)
    tokens, invalids, counts = lexer.lex()

    print(f"Input: {line}")
    print_token_stream(tokens)
    print_invalids(invalids)
    print_counts(counts)