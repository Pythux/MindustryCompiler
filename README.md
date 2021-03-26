
# MindustryCompiler

[![Latest Version](https://img.shields.io/pypi/v/PyBoa.svg)](https://pypi.python.org/pypi/MindustryCompiler/)

compile to mindustry asm code,

the language is a subset of mindustry asm code [named Mindustry Logic](https://github.com/MindustryGame/wiki/blob/master/docs/logic/0-introduction.md)

## features

- all mindustry code are valide as it

- jump to a reference:

    ```plain
    ...
    jump bottom always true true  <--- jump to #ref bottom
    ...
    #ref bottom  <--- set ref anywhere
    ...
    ```

- comments:

    ```plain
    // this is a comment

    #ref loop // another comment after some blank lines
    ```

## comming soon

- improve jump conition:

- if condition:

- else, else if:

- multiple condition:

- function:

## current usage

- compile a file :

    ```sh
    > mindc fileName
    ```

    exemple, in this folder:

    ```sh
    > mindc tests/identicalCode/3-comments.code
    ```

- get the result in clipboard to just past it in mindustry :

    ```sh
    > mindc --ctrlC tests/identicalCode/3-comments.code
    ```

- run interactive to play with it :

    ```sh
    > mindc --interactive
    ```

## Installation

### you need python to run this software

- check that you have it

    type in your shell/terminal :

    ```sh
    python3 --version
    ```

    must give you something like: `Python 3._._`

- if you don't have it, install it :

    you could dowload python from [here](https://www.python.org/downloads/release)

### install mindustry compiler

- with python package manager:

    ```sh
    python3 -m pip install ___
    ```

    to run it, type:

    ```sh
    mindc
    ```

- or download this git and run `__main__.py` file
    to run it:

    ```sh
    python3 compiler/__main__.py
    ```
