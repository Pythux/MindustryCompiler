set message message1
print "hi !, what is the value of x and y ?"
printflush message
set tmp5 1.6
op add returnAddress-None-wait @counter 1
jump 26 always true true
set x @thisx
set y @thisy
print "x:"
print x
print " y:"
print y
set tmp1 "\n and now we will wait two secondes"
set tmp3 message
op add returnAddress-None-printAndWait @counter 1
jump 31 always true true
set tmp1 "2s have passed !"
set tmp3 message
op add returnAddress-None-printAndWait @counter 1
jump 31 always true true
set tmp2 "we could also use tmpX variables freely"
set tmp1 tmp2
set tmp3 message
op add returnAddress-None-printAndWait @counter 1
jump 31 always true true
end
set tmp4 @time
op mul tmp5 tmp5 1000
op add tmp6 tmp4 tmp5
jump 29 greaterThanEq tmp6 @time
set @counter returnAddress-None-wait
print tmp1
printflush tmp3
set tmp5 2
op add returnAddress-None-wait @counter 1
jump 26 always true true
set @counter returnAddress-None-printAndWait
