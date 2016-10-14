func gcd(a int = 10, b int) {
	return gcd(b,a%b);
}

print gcd(3178, 252);
