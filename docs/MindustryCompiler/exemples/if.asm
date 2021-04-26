sensor in node1 @powerNetIn
sensor out node1 @powerNetOut
op sub net in out
op floor net net out
print "power: "
print net
printflush message1
jump 13 greaterThanEq net 1200
jump 11 greaterThanEq net 500
draw clear 1000 0 0 0 0 0
jump 14 always true true
draw clear 1000 1000 0 0 0 0
jump 14 always true true
draw clear 0 1000 0 0 0 0
drawflush display1
set wait 0
op add wait wait 1
jump 16 lessThanEq wait 200
