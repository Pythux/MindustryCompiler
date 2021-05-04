set m message1
set tmp1 "hi!"
set tmp2 m
op add returnAddress-None-show @counter 1
jump 10 always true true
set tmp1 "how are you"
set tmp2 m
op add returnAddress-None-show @counter 1
jump 10 always true true
end
print tmp1
printflush tmp2
set @counter returnAddress-None-show
