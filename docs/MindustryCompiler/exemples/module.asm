set message message1
set tmp1 "hey !"
set tmp2 message
op add returnAddress-msg-printAndWait @counter 1
jump 10 always true true
set tmp1 "do you read this ?"
set tmp2 message
op add returnAddress-msg-printAndWait @counter 1
jump 10 always true true
end
print tmp1
printflush tmp2
set tmp4 2
op add returnAddress-time-wait @counter 1
jump 16 always true true
set @counter returnAddress-msg-printAndWait
set tmp3 @time
op mul tmp4 tmp4 1000
op add tmp5 tmp3 tmp4
jump 19 greaterThanEq tmp5 @time
set @counter returnAddress-time-wait
