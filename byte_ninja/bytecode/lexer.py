from .token import (
    TOKEN_DEFS,
    Token,
    TokenType,
    WHITESPACE,
    TOK_EOF,
)


def tokenize(source: str) -> list[Token]:
    """ Tokenize source code. """

    stack = list()
    lineno = 1
    ws = ''

    while source:
        # strip whitespace
        m = WHITESPACE.match(source)
        source = source[m.span()[-1]:]

        # update line numbers
        ws = m.group()
        lineno += ws.count('\n')

        if not source:
            break

        # parse a single token
        for token_def in TOKEN_DEFS:
            m = token_def.value.match(source)

            if m is None:
                continue

            source = source[m.span(m.lastindex)[-1]:]
            stack.append(Token(
                typ=token_def.type,
                # last group should be only the value
                value=m.group(m.lastindex),
                lineno=lineno,
                whitespace=ws,
            ))
            break
        else:
            # no token matched
            raise SyntaxError(f'invalid syntax {repr(source)}')

    stack.append(
        Token(
            typ=TOK_EOF,
            value='',
            lineno=lineno,
            whitespace=ws,
        )
    )

    return stack
