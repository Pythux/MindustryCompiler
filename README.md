# Mindustry-ASM

compiler that transforme to mindustry asm code


## Installation:

### need python

install python here

#### pip

have `pip` ? pip install ...

run it with `> mindc` command

#### whitout pip

dowload this project

run it with:

 `> python compiler/__main__.py`

## current usage

### compile a file

`> mindc fileName`

### get the result in clipboard to just past it in mindustry

`> mindc --ctrlC fileName`

### run interactive to play with it

`> mindc --interactive`

```
> #ref start
> set result 1
> #ref loopAdd
> add result 1 1
> jump start equal result 4
> jump loopAdd
```
