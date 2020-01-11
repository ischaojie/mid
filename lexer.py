from ply.lex import lex, TOKEN
from ply.yacc import yacc

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
# the markdown contents token
@TOKEN(r'([0-9a-zA-Z\u4e00-\u9fa5]|[., :;/\'’?{}"\\+^#|=%&])+')
def t_TEXT(t):
    return t


@TOKEN(r'[\n\r]{1}[#]{1,6}')
def t_POUND(t):
    """header token"""
    t.value = str(len(t.value) - 1)
    return t


@TOKEN(r'[>]{1}')
def t_QUOTE(t):
    """quote token"""
    return t


@TOKEN(r'[\n\r]{1}[\t]*[\*\-\+]{1}[ ]{1}')
def t_LISTDASH(t):
    """the list"""
    t.value = t.value[1:-1]
    return t


@TOKEN(r'[\n\r]{1}[\t]*[0-9]+[.]{1}[0-9]*[ ]{1}')
def t_LISTNUMBER(t):
    """the number list"""
    t.value = t.value[1:-1]
    return t


@TOKEN(r'[*_]{2}')
def t_BOLD(t):
    return t


@TOKEN(r'[*_]{1}')
def t_ITALIC(t):
    return t


@TOKEN(r'[`]{1}')
def t_CODE(t):
    return t


@TOKEN(r'[\n\r]{1}[ ]{0,1}[`]{3}[ ]{0,}')
def t_CODEFIELD(t):
    t.value = t.value[1:]
    return t


@TOKEN(r'[ ]{0,1}[!]{1}')
def t_POINT(t):
    return t


@TOKEN(r'[\(]{1}')
def t_LPAREN(t):
    """( token"""
    return t


@TOKEN(r'[\)]{1}')
def t_RPAREN(t):
    """) token"""
    return t


@TOKEN(r'[\[]{1}')
def t_LBRACKET(t):
    """[ token"""
    return t


@TOKEN(r'[\]]{1}')
def t_RBRACKET(t):
    """] token"""
    return t


@TOKEN(r'[\n\r]')
def t_LINE(t):
    t.value = len(t.value)
    return t


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


@TOKEN(r'\n+')
def t_newline(t):
    t.lexer.lineno += t.value.count("\n")


# Ignored characters
# t_ignore = r'\s+'

lexer = lex()
# Test it out
data = '''
# header1
## header2
### header3


paragraph paragraph paragraph paragraph paragraph paragraph, paragraph
paragraph paragraph paragraph paragraph paragraph paragraph.

中文测试

> I am iron man.

- test1
- test2
+ test3
* test4


1. num
1.1 list
2. ddd

number2 **bold** hero *italic* use lexer, and parser.dsdsd[google](google.com)

I stupid write this: `this is a code`, but.![google](google.com)

```
def index():
    print(hello)
```

'''

# Give the lexer some input
lexer.input(data)

# Tokenize
while True:
    tok = lexer.token()
    if not tok:
        break  # No more input
    print(tok)
