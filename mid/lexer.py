from mid.ply import lex
from mid.ply.lex import TOKEN

tokens = (
    'TEXT',  # md contents
    'LINE',  # new line

    'POUND',  # #
    'QUOTE',  # >
    'LISTDASH',  # * + -
    'LISTNUMBER',  # 1. 2.

    'BOLD',  # **
    'ITALIC',  # *
    'CODE',  # `
    'CODEFIELD',  # ```
    'POINT',  # !

    'LPAREN',  # (
    'RPAREN',  # )
    'LBRACKET',  # [
    'RBRACKET',  # ]
)


# todo: match all language
# todo: 中文标点符号处理
# the markdown contents token
@TOKEN(r'([0-9a-zA-Z\u4e00-\u9fa5]|[., :;/\'’?{}<"\\+^|=%&\-])+')
def t_TEXT(t):
    return t


@TOKEN(r'\n{0,1}\#{1,6}')
def t_POUND(t):
    """header token"""

    # 如果header前面有换行
    if t.value[0] == '\n':
        t.value = str(len(t.value) - 1)
    else:
        t.value = str(len(t.value))
    return t


@TOKEN(r'\n{0,1}\>')
def t_QUOTE(t):
    """quote token"""
    t.value = t.value[1:]
    return t


@TOKEN(r'[\n\r][\t]*[\*\-\+]{1}[ ]{1}')
def t_LISTDASH(t):
    """the list"""
    t.value = t.value[1:-1]
    return t


@TOKEN(r'[\n\r]{1}[\t]*[0-9]+[.]{1}[0-9]*[ ]{1}')
def t_LISTNUMBER(t):
    """the number list"""
    t.value = t.value[1:-1]
    return t


@TOKEN(r'\*\*')
def t_BOLD(t):
    return t


@TOKEN(r'\*')
def t_ITALIC(t):
    return t


@TOKEN(r'\`')
def t_CODE(t):
    return t


@TOKEN(r'[\n\r]{1}[ ]{0,1}[`]{3}[ ]{0,}')
def t_CODEFIELD(t):
    t.value = t.value[1:]
    return t


@TOKEN(r'\!|\！')
def t_POINT(t):
    """point: !"""
    return t


@TOKEN(r'\(')
def t_LPAREN(t):
    """( token"""
    return t


@TOKEN(r'\)')
def t_RPAREN(t):
    """) token"""
    return t


@TOKEN(r'\[')
def t_LBRACKET(t):
    """[ token"""
    return t


@TOKEN(r'\]')
def t_RBRACKET(t):
    """] token"""
    return t


@TOKEN(r'[\n\r]')
def t_LINE(t):
    """line"""
    t.value = len(t.value)
    return t


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


@TOKEN(r'\n+')
def t_newline(t):
    t.lexer.lineno += t.value.count("\n")


def test_lexer():
    import os
    readme = os.path.join(os.path.abspath('.'), 'README.md')
    lexer = lex.lex(debug=1)
    with open(readme, 'r') as fp:
        data = fp.read()

    lexer.input(data)
    # Tokenize
    while True:
        tok = lexer.token()
        if not tok:
            break  # No more input
        print(tok)


test_lexer()
