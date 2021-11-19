
# MindustryCompiler

a langage that compile to mindustry asm code know as mindustry-logic,

What's mindustry-logic ? Here is a nice starting guide with in game screenshots:
[How To Use Procesors in 6.0](https://steamcommunity.com/sharedfiles/filedetails/?id=2268059244)

The language created here is a superset of mindustry-logic code

here's the [website](https://pythux.github.io/MindustryCompiler) to show features in actions and compile your code

## features

- all mindustry-logic code are valide as it

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

You could check files [here](./tests/identicalCode) to see the difference from the same programme that compile to the same mindustry-logic

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
    add(a, b)
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

- static for loop:

    ```plain
    import msg

    set message message1

    for x, y in [(1, 2), (4, 3)]
        if x > y
            print "x : "
            print x
            print " higher than: "
            msg.printAndWait(y, message)
    ```

- look [files here](./code/bots) for some code exemple that I use

## coming soon

- afectation `a = 1` and simple operation +, -, /, *, ...

- operation += -=

- improve if, if var, if not var, and / or

- fill empty args of ASM lines (`ucontrol itemDrop store 800 0 0 0` -> `ucontrol itemDrop store 800`)

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
