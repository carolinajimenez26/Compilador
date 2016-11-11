//no debe graficar la funcion
func gcd(a int, b int) string {
	return gcd(b,a%b);
}

print gcd(3178, 252);
