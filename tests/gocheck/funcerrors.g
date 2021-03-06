/* funcerrors.g

   Checks of some common errors with functions */

func add(x int, y int) int {
	return x + y;
}

func main() int {
	var r int;
	r = add();          // Not enough args
	r = add(2,3,4);     // Too many args
	r = add(2,3.5);     // Type error in arg 2
	var fr float;
	fr = add(2,3);      // Type error in assignment
	fr = sub(3.4,2.5);  // Undefined function
	fr = r(2,3);        // Not a function
}

func error1(x int) int {
	return 3.5;          // Type error on return
}

func error2(x bar) int {  //Undefined type 'bar'
	return 0;
}

func error3(x int) bar { // Undefined return type 'bar'
	var q int = 4;
	return 0;
}

print q;  // undefined identifer (out of scope)

func error4(x int) int {  // no return statement

}

func error5(x int) int {
	func error6(x int) int {  // nested
		return 0;
	}
	return 0;
}
