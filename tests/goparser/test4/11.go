// Este no debe graficarlo
/*func pow(lim float) float {
	if v := pow(x, n); v < lim {
		return v
	}
	return lim
}*/

// Este debe graficarlo

var v float =1.1;
func pow(lim float) float {
	if v < lim {
		return v
	}
	return lim
}

func main() int {
	pow(3, 2, 10);
	pow(3, 3, 20);
}
