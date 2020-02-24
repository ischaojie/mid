# mid
Hi！ I am mid, I am a ## markdown compiler, you can use
me convert markdown document > to html file.

now: under construction ！! !

> Thanks ply.

## Todo
- mathematical formula support
- code field support

## Feature

- support '#' for header
- support '+ - *' for unordered and '1. 2.' for ordered list
- support '>' for quote
- support '\*\*' for **bold** and '*' for *italic*
- support '\`' for `code`
- support '```' for code field
- support '\[\]()' for [url](https://github.com/shiniao/)
- support '!\[\]()' for image

## How to use?
1. You can used mid on the command line :

```
> mid <foo.md> <boo.html>

# type mid -h for more information
> mid -h
```

2. by api:
```
html = mid.convert('hakuna.md')
print(html)
``` 

##License

MIT

