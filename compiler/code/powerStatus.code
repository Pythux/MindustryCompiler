sensor in node1 @powerNetIn
sensor out node1 @powerNetOut
print "power status: "
op sub net in out
jump 10 greaterThanEq net 1000
jump 14 lessThan net 200
draw clear 1000 1000 0 0 0 0
drawflush display1
print "[yellow]"
jump 17 always x false
draw clear 0 1000 0 255 0 0
drawflush display1
print "[green]"
jump 17 always x false
draw clear 1000 0 0 0 0 0
drawflush display1
print "[red]"
print net
printflush message1
set wait 0
op add wait wait 1
jump 20 lessThanEq wait 200
