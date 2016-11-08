func mod(a int, b int) int {
	if b==0 {
		return a;
	}
	return a-(a/b)*b;
}

func gcd(a int, b int) int {
	if b==0 {
		return a;
	}
	return gcd(b, mod(a,b));
}

var a int=2130;
var b int=512;
print gcd(a,b);