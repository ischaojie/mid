import mid

with open('README.md', 'r') as fp:
    markdown = fp.read()

html = mid.convert(markdown)

print(html)
