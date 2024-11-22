from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional, Any
from .terms import Term, Var, Not, And, Or, Xor, Equal, Arrow


class TokenType(Enum):
    VAR = auto()  # A, B, C, ...
    NOT = auto()  # !
    AND = auto()  # *
    OR = auto()  # |
    XOR = auto()  # +
    IMPLIES = auto()  # >
    EQUALS = auto()  # =
    LPAREN = auto()  # (
    RPAREN = auto()  # )
    EOF = auto()


@dataclass
class Token:
    type: TokenType
    value: str
    pos: int


class ParserError(Exception):
    def __init__(self, message: str, pos: int):
        self.message = message
        self.pos = pos
        super().__init__(f"{message} at position {pos}")


class Parser:
    """
    Parser for logical expressions using recursive descent with precedence rules.
    Supports operators: !, *, |, +, >, = with proper precedence.
    """

    def __init__(self):
        # Operator precedence (higher = higher precedence)
        self.precedence = {
            TokenType.NOT: 5,
            TokenType.AND: 4,
            TokenType.OR: 3,
            TokenType.XOR: 2,
            TokenType.IMPLIES: 1,
            TokenType.EQUALS: 0,
        }

    def tokenize(self, expression: str) -> list[Token]:
        """Convert input string to list of tokens"""
        tokens = []
        pos = 0
        expression = expression.replace(' ', '')  # Remove whitespace

        while pos < len(expression):
            char = expression[pos]

            if char.isalpha():
                if not char.isupper():
                    raise ParserError("Variables must be uppercase letters", pos)
                tokens.append(Token(TokenType.VAR, char, pos))
            elif char == '!':
                tokens.append(Token(TokenType.NOT, char, pos))
            elif char == '*':
                tokens.append(Token(TokenType.AND, char, pos))
            elif char == '|':
                tokens.append(Token(TokenType.OR, char, pos))
            elif char == '+':
                tokens.append(Token(TokenType.XOR, char, pos))
            elif char == '>':
                tokens.append(Token(TokenType.IMPLIES, char, pos))
            elif char == '=':
                tokens.append(Token(TokenType.EQUALS, char, pos))
            elif char == '(':
                tokens.append(Token(TokenType.LPAREN, char, pos))
            elif char == ')':
                tokens.append(Token(TokenType.RPAREN, char, pos))
            else:
                raise ParserError(f"Unexpected character: {char}", pos)

            pos += 1

        tokens.append(Token(TokenType.EOF, '', pos))
        return tokens

    def parse(self, expression: str) -> Term:
        """Main parse function"""
        try:
            tokens = self.tokenize(expression)
            result, pos = self._parse_expr(tokens, 0, 0)

            if pos >= len(tokens) or tokens[pos].type != TokenType.EOF:
                raise ParserError("Unexpected tokens after expression", tokens[pos].pos)

            return result

        except ParserError as e:
            # Enhance error message with visual pointer
            pointer = ' ' * e.pos + '^'
            raise ParserError(f"{e.message}\n{expression}\n{pointer}", e.pos)

    def _parse_expr(self, tokens: list[Token], pos: int, min_precedence: int) -> tuple[Term, int]:
        """Parse expression with operator precedence"""
        term, pos = self._parse_primary(tokens, pos)

        while pos < len(tokens):
            token = tokens[pos]

            if token.type in (TokenType.RPAREN, TokenType.EOF):
                break

            if token.type not in self.precedence:
                raise ParserError(f"Expected operator, got: {token.value}", token.pos)

            if self.precedence[token.type] < min_precedence:
                break

            op_token = token
            pos += 1

            right_term, new_pos = self._parse_expr(
                tokens,
                pos,
                self.precedence[op_token.type] + 1
            )

            # Create appropriate Term based on operator
            if op_token.type == TokenType.AND:
                term = And(term, right_term)
            elif op_token.type == TokenType.OR:
                term = Or(term, right_term)
            elif op_token.type == TokenType.XOR:
                term = Xor(term, right_term)
            elif op_token.type == TokenType.IMPLIES:
                term = Arrow(term, right_term)
            elif op_token.type == TokenType.EQUALS:
                term = Equal(term, right_term)
            else:
                raise ParserError(f"Unhandled operator: {op_token.value}", op_token.pos)

            pos = new_pos

        return term, pos

    def _parse_primary(self, tokens: list[Token], pos: int) -> tuple[Term, int]:
        """Parse primary expressions (variables, negations, parenthesized expressions)"""
        if pos >= len(tokens):
            raise ParserError("Unexpected end of input", pos)

        token = tokens[pos]

        if token.type == TokenType.VAR:
            return Var(token.value), pos + 1

        elif token.type == TokenType.NOT:
            term, new_pos = self._parse_primary(tokens, pos + 1)
            return Not(term), new_pos

        elif token.type == TokenType.LPAREN:
            term, new_pos = self._parse_expr(tokens, pos + 1, 0)

            if new_pos >= len(tokens) or tokens[new_pos].type != TokenType.RPAREN:
                raise ParserError("Missing closing parenthesis", token.pos)

            return term, new_pos + 1

        raise ParserError(
            f"Expected variable, negation, or parenthesized expression, got: {token.value}",
            token.pos
        )


def parse(expression: str) -> Term:
    """Convenience function to parse logical expressions"""
    return Parser().parse(expression)
