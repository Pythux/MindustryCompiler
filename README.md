
# MindustryCompiler

a langage that compile to mindustry asm code,

What's mindustry asm ? Here is a nice starting guide with in game screenshots:
[How To Use Procesors in 6.0](https://steamcommunity.com/sharedfiles/filedetails/?id=2268059244)

The language created here is a superset of what I call mindustry asm code [named Mindustry Logic by it's creator](https://github.com/MindustryGame/wiki/blob/master/docs/logic/0-introduction.md)

## features

- all mindustry asm code are valide as it

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

- improve jump conition:

    ```plain
    jump loop  // <--- jump loop always true true
    jump inf 2 < 4  // <--- jump inf lowerThan 2 4

    // ==, ===, !=, >, >=, <, <=, ---> equal, notEqual, greaterThan, ...
    ```

You could check files [here](./tests/identicalCode) to see the difference from the same programme that compile to the same mindustry asm

- if else, else if condition:

    ```plain
    if 2 < 4
        print "2 < 4"
    else if 2 == 1
        print "2 == 1"

    elif 2 === 2  // "elif" is equivalent to "else if"
        print "2 === 2"

    else
        print "else"
    ```

- function:

    ```plain
    def add(a, b)
        add result a b
        return result

    x = 0
    x = add(x, 2)
    ```

- module:

    ```plain
    import time

    time.wait(2)  // wait 2 secondes
    ```

## coming soon

- ...

## current usage

- compile a file :

    ```sh
    mindc fileName
    ```

    exemple, in this folder:

    ```sh
    mindc tests/identicalCode/4-improveJump.code
    ```

- get the result in clipboard to just past it in mindustry :

    ```sh
    mindc tests/identicalCode/4-improveJump.code --ctrlC
    ```

- run interactive to play with it :

    ```sh
    mindc --interactive
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

```sh
python3 -m pip install MindustryCompiler
```

### run it

```sh
mindc
```
