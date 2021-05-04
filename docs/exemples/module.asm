set m message1
set tmp1 "hey"
set tmp2 m
op add returnAddress-msg-printAndWait @counter 1
jump 14 always true true
set tmp1 "yo"
set tmp2 m
op add returnAddress-msg-printAndWait @counter 1
jump 14 always true true
set tmp1 "y good ?"
set tmp2 m
op add returnAddress-msg-printAndWait @counter 1
jump 14 always true true
end
print tmp1
printflush tmp2
set tmp3 2
op add returnAddress-time-wait @counter 1
jump 20 always true true
set @counter returnAddress-msg-printAndWait
set tmp4 @time
op mul tmp3 tmp3 1000
op add tmp5 tmp4 tmp3
jump 23 greaterThanEq tmp5 @time
set @counter returnAddress-time-wait
