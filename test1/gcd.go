func gcd(x:int, y:int) int
g: int
g = y
while x > 0
g = x;
x = y - (y/x) * x;
y = g
return g