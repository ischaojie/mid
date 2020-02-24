"""""""""""""""""""""""""""""""""""""""""""""""
--------     the markdown parser     --------
"""""""""""""""""""""""""""""""""""""""""""""""

"""
THis is the markdown parse section.

"""

from mid.ply import yacc
from mid.lexer import tokens

precedence = (
    ('left', 'PRIORITY0'),
    ('left', 'PRIORITY1'),
    ('left', 'PRIORITY2'),
)

"""
(root node) ast node looks like:
md : md head
md : md line paragraph  // paragraph need start at new +line
md : md line 
md : md quote
md : md list
md : md codefield line CODEFIELD
md : md image
md : md math

head : POUND contents
quote : line QUOTE paragraph
image : line POINT LBRACKET contents RBRACKET LPAREN contents RPAREN
list : 
codefield:

paragraph : paragraph contents
paragraph : paragraph BOLD contents BOLD
paragraph : paragraph ITALIC contents ITALIC
paragraph : paragraph CODE contents CODE
paragraph : paragraph LBRACKET contents RBRACKET LPAREN contents RPAREN

contents: TEXT
    
this nodes all need start at new line.
"""


# header1 header2 or ...
# need header node
def p_md_head(p):
    'md : md head'
    p[0] = '{}{}\n'.format(p[1], p[2])


# paragraph
# need (line paragraph) node
def p_md_paragraph(p):
    'md : md line paragraph %prec PRIORITY0'
    p[0] = "{}<p>{}</p>\n".format(p[1], p[3])


# code field
# need (code-field line) node
def p_md_codefield(p):
    'md : md codefield line CODEFIELD %prec PRIORITY0'
    p[0] = "{}{}\n</code></pre>".format(p[1], p[2])


# todo: 引用间有空行，则新的引用标签
# quote
# need quote node
def p_md_quote(p):
    'md : md quote'
    if p[1][-18:] == "</p></blockquote>\n":
        p[0] = p[1][:-18] + p[2][:-17] + p[1][-18:]
    else:
        p[0] = '{}<blockquote><p>{}\n'.format(p[1], p[2])


def p_md_image(p):
    'md : md image'
    p[0] = '{}{}\n'.format(p[1], p[2])


def p_md_line(p):
    'md : md line'
    p[0] = p[1] + p[2]


def p_md_empty(p):
    'md : empty'
    p[0] = p[1]


# todo: 有序列表start=指定数字
def p_md_listnumber(p):
    'md : md listnumber'
    if p[1][-6:] == '</ol>\n':
        p[0] = p[1][:-6] + p[2]
    else:
        p[0] = '{}<ol>{}'.format(p[1], p[2])


def p_listnumber(p):
    'listnumber : LISTNUMBER paragraph'
    p[0] = '<li>{}</li></ol>\n'.format(p[2])


def p_md_listdash(p):
    'md : md listdash'
    if p[1][-6:] == '</ul>\n':
        p[0] = p[1][:-6] + p[2]
    else:
        p[0] = '{}<ul>{}'.format(p[1], p[2])


def p_listdash(p):
    'listdash : LISTDASH paragraph'
    p[0] = '<li>{}</li></ul>\n'.format(p[2])


"""code field"""


def p_codefield_paragraph(p):
    'codefield0 : codefield paragraph'
    p[0] = p[1] + [2] + '\n'


def p_codefield0_paragraph(p):
    'codefield0 : codefield0 paragraph'
    p[0] = p[1] + [2] + '\n'


def p_codefield_line(p):
    'codefield : codefield line line'
    p[0] = p[1] + '\n'


def p_codefield0_line(p):
    'codefield : codefield0 line line'
    p[0] = p[1] + '\n'


def p_codefield0_create(p):
    'codefield0 : line CODEFIELD'
    p[0] = "<pre><code>"


"""paragraph contain contents
paragraph:
    TEXT

"""


def p_paragraph_contents(p):
    'paragraph : paragraph contents %prec PRIORITY1'
    p[0] = p[1] + p[2]


# [url](address)
# url in contents
def p_contents_url(p):
    'paragraph : paragraph LBRACKET contents RBRACKET LPAREN contents RPAREN %prec PRIORITY2'
    p[0] = '{}<a href="{}">{}</a>'.format(p[1], p[6], p[3])


# bold
def p_contents_bold(p):
    'paragraph : paragraph BOLD contents BOLD %prec PRIORITY2'
    p[0] = '{}<b>{}</b>'.format(p[1], p[3])


# italic
def p_contents_italic(p):
    'paragraph : paragraph ITALIC contents ITALIC %prec PRIORITY2'
    p[0] = '{}<i>{}</i>'.format(p[1], p[3])


# code
def p_contents_code(p):
    'paragraph : paragraph CODE contents CODE %prec PRIORITY2'
    p[0] = '{}<code>{}</code>'.format(p[1], p[3])


# def p_paragraph_add_notation(p):
#     '''paragraph : paragraph POINT contents %prec PRIORITY1
#
#                 | paragraph ITALIC contents %prec PRIORITY1
#                 | paragraph CODE contents %prec PRIORITY1'''
#
#     p[0] = p[1] + p[2] + p[3]
#
#
# def p_paragraph_add_point(p):
#     'paragraph : paragraph POINT line %prec PRIORITY1'
#     p[0] = p[1] + p[2]


def p_paragraph_empty(p):
    'paragraph : contents'
    p[0] = p[1]


def p_contents_text(p):
    'contents : TEXT'
    p[0] = p[1]


"""""""single node"""""""


# # header
# POUND get the header level.
def p_head(p):
    'head : POUND TEXT'
    p[0] = "<h{}>{}</h{}>".format(p[1], p[2], p[1])


# ![image](addr)
#
def p_image(p):
    'image : line POINT LBRACKET TEXT RBRACKET LPAREN TEXT RPAREN %prec PRIORITY2'
    p[0] = '<img src="{}", alt="{}">'.format(p[7], p[4])


# >
# (line, QUOTE paragraph)
def p_quote(p):
    'quote : line QUOTE paragraph %prec PRIORITY2'
    p[0] = p[3] + "</p></blockquote>"


# black line
# match a black line.
def p_line(p):
    'line : LINE'
    p[0] = ""


def p_empty(p):
    'empty : '
    p[0] = ""


def p_error(p):
    print("Syntax error at {}-{}".format(p.type, p.value))


my_parse = yacc.yacc()


def parse(data):
    res = my_parse.parse(data, tracking=True)
    return res
