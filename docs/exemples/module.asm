set tmp1 1
op add returnAddress-time-wait @counter 1
jump 10 always true true
set tmp1 1.5
op add returnAddress-time-wait @counter 1
jump 10 always true true
set tmp1 2
op add returnAddress-time-wait @counter 1
jump 10 always true true
end
set tmp2 @time
op mul tmp1 tmp1 1000
op add tmp3 tmp2 tmp1
jump 13 greaterThanEq tmp3 @time
set @counter returnAddress-time-wait
