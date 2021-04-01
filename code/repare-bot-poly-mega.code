sensor locx point1 @x
sensor locy point1 @y
op rand rand 1 0
jump 6 equal rand 0
ubind @poly
jump 7 always true true
ubind @mega
sensor h @unit @health
sensor hm @unit @maxHealth
op div hper h hm
op greaterThan result hper 0.75
jump 13 equal result true
ucontrol move locx locy 0 0 0
end
