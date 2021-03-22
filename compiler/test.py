#!/usr/bin/env python


from typing import List


def main():
    content = ""
    with open('yo.code') as fd:
        content = fd.read()
    handleContent(content)


def spacer():
    for _ in range(3):
        print('#'*6)


def handleContent(content):
    print(content)
    spacer()
    content = delComAndEmpty(content)
    print(content)


def delComAndEmpty(content: str) -> List[str]:
    lines = content.split('\n')
    index = -1
    while len(lines) > index:
        index += 1
        if lines[index] == '' or lines[index].startswith('//'):
            del lines[index]
    return lines


main()
