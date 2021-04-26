set a 1
set b 2
set c 3
op add a a 1
print a
print " "
op add b b 1
print b
print " "
op add c c 1
print c
print " "
set tmp2 1
op add returnAddress-time-wait @counter 1
jump 18 always true true
printflush message1
jump 3 always true true
end
set tmp1 @time
op mul tmp2 tmp2 1000
op add tmp3 tmp1 tmp2
jump 21 greaterThanEq tmp3 @time
set @counter returnAddress-time-wait
