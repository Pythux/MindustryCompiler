
set message message1
ubind @flare
jump 4 equal @unit null
jump 5 always true true
end
sensor botType @unit @type
jump 8 equal procId null
jump 11 always true true
op add returnAddress-idBots-genProcId @counter 1
jump 41 always true true
set procId tmp3
jump 28 always true true
set tmp21 procId
set tmp17 botType
set tmp16 message
op add returnAddress-idBots-tryTakeOneMoreBot @counter 1
jump 50 always true true
set haveNewBot tmp19
jump 20 equal haveNewBot true
jump 28 always true true
jump 22 equal bot1 null
jump 24 always true true
set bot1 @unit
jump 28 always true true
jump 26 equal bot2 null
jump 28 always true true
set bot2 @unit
jump 28 always true true
set radiusApproche 5
jump 31 equal bot1 null
jump 32 always true true
jump 12 always true true
ubind bot1
ucontrol approach @thisx @thisy radiusApproche null null
jump 36 equal bot2 null
jump 37 always true true
jump 12 always true true
ubind bot2
ucontrol approach @thisx @thisy radiusApproche null null
jump 28 always true true
end
op rand tmp1 999 tmp2
op floor tmp1 tmp1 tmp2
jump 45 lessThan tmp1 100
jump 47 always true true
op mul tmp1 tmp1 10
jump 43 always true true
set tmp3 tmp1
jump 49 always true true
set @counter returnAddress-idBots-genProcId
print "[white] need some more bots"
printflush tmp16
ubind tmp17
jump 55 equal @unit tmp18
jump 63 always true true
print "[yellow] no bots of the choosen type anymore, \n"
print "you can pick another kind of bot in the instruction 'ubind' at the begining of the programme"
set tmp22 ""
set tmp23 tmp16
op add returnAddress-msg-printAndWait @counter 1
jump 74 always true true
set tmp19 tmp18
jump 73 always true true
sensor tmp20 @unit @flag
jump 66 equal tmp20 0
jump 71 always true true
ucontrol flag tmp21 tmp18 tmp18 tmp18 tmp18
print "[green] free bot found !"
printflush tmp16
set tmp19 @unit
jump 73 always true true
set tmp19 tmp18
jump 73 always true true
set @counter returnAddress-idBots-tryTakeOneMoreBot
print tmp22
printflush tmp23
set tmp25 2
op add returnAddress-time-wait @counter 1
jump 80 always true true
set @counter returnAddress-msg-printAndWait
set tmp24 @time
op mul tmp25 tmp25 1000
op add tmp26 tmp24 tmp25
jump 83 greaterThanEq tmp26 @time
set @counter returnAddress-time-wait
