from compiler import markdown

md = """
# header1
## header2
### header3

paragraph paragraph paragraph paragraph paragraph paragraph, paragraph
paragraph paragraph paragraph paragraph paragraph paragraph.

中文测试

> I am iron man.
> quote 2

> quote3

- test1
- test2
+ test3
* test4


1. num
1.1 list
2. ddd

number2 paragraph **bold** hero mine this is *italic* use lexer, and parser,
should give up hah, and use what [url](https://baidu.com) like this.

I stupid write this: `this is a code`, but.

![sdsd](https://baidu.com)


"""
print(markdown(md))
