

from .tokens import Token


def tokenize(s):

    if not isinstance(s, basestring):
        raise Exception("Cannot parse a non-string value: {}: {}".format(type(s), s))

    tokens = []
    value = ''
    state = Token.string

    for c in s:

        if c == '<':

            if state == Token.string:

                state = Token.lookup

                if value:
                    tokens.append(Token(value, Token.string))

                value = ''

            continue

        elif c == '#':

            if state == Token.lookup and value == '':

                state = Token.action

            continue

        elif c == '>':

            if state == Token.lookup or state == Token.action:

                tokens.append(Token(value, state))

                state = Token.string

                value = ''

            continue

        value += c

    if value:
        tokens.append(Token(value, state))

    return tokens
