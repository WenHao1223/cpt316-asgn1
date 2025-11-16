# COMPY Mini-Compiler

## 1.0 Programming Paradigm & Justification

This mini-compiler for the COMPY language uses a **hybrid design**:
- **Object-Oriented Programming (OOP)** is the primary paradigm, providing modularity and encapsulation.
- **Procedural Programming** supports linear control flow and helper routines.

### 1.1 Object-Oriented Programming (OOP)

Key compiler concepts are implemented as classes:
- **Token** (`token_module.py`): Represents a lexical unit (type, lexeme, position).
- **Lexer** (`lexer_module.py`): Handles tokenization and scanning state.
- **Syntax** (`syntax_module.py`): Implements a recursive-descent parser, mapping grammar rules to methods.
- **ParseTree** (`tree_module.py`): Models nodes in parse and syntax trees.

### 1.2 Procedural Programming

Procedural code is used for:
- Running the compiler pipeline in `main.py` (input → lex → parse → output).
- Helper functions and tree export routines (`export_tree_module.py`).

### 1.3 Why OOP Is Suitable

- **Separation of Phases:** Lexer, parser, and tree are independent classes.
- **Encapsulation:** Each stage hides its complexity.
- **Reusability:** Easily extendable for new tokens or grammar rules.
- **Maintainability:** Modular design supports isolated development and debugging.

## 2.0 Design & Implementation

### 2.1 Lexical Analyzer

The lexer transforms source code into a stream of tokens:
- **Token Types:** Identifier, Number, Operator, Assignment, Parenthesis, Statement Terminator.
- **Tokenization:** Uses regular expressions to classify input characters.
- **Invalid Token Handling:** Invalid characters are reported with position info.
- **Token Counting:** Displays counts for each token type and invalids.

### 2.2 Syntax Analyzer

The parser checks token sequences against grammar rules and builds trees:
- **Recursive Descent Parsing:** Each grammar rule is a method in `Syntax`.
- **Statement Parsing:** Handles assignments and expressions.
- **Expression Parsing:** Supports addition and subtraction.
- **Term Parsing:** Supports multiplication and division.
- **Factor Parsing:** Handles numbers, identifiers, and parenthesized expressions.

### 2.3 Tree Visualization

- **Parse Tree:** Shows full grammar structure.
- **Syntax Tree:** Shows essential syntactic relationships.
- Trees are displayed in the terminal and exported as PNG files (`output/line-<N>-parse-tree.png`, `output/line-<N>-syntax-tree.png`).

## 3.0 Error Handling

- **Lexical Errors:** Reported for invalid characters during tokenization.
- **Syntax Errors:** Reported for grammar mismatches during parsing, using the `expect()` method.
