import os

import mid

readme = os.path.join(os.path.abspath('.'), 'README.md')


def markdown() -> str:
    with open(readme, 'r') as fp:
        md = fp.read()
    return md


def test_lexer():
    pass


def test_md():
    md = markdown()
    with open('test.html', 'w+') as f:
        f.write(mid.convert(md))
        print("convert html ok!")


test_md()
