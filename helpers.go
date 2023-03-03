package main

// https://dai.fmph.uniba.sk/upload/e/ee/Cg1_Prieniky.pdf
// druhý spôsob

func d(A Position, B Position, C Position) float32 {
	return A.X*(B.Y-C.Y) + A.Y*(C.X-B.X) + B.X*C.Y - B.Y*C.X
}

func intersect(A1 Position, A2 Position, B1 Position, B2 Position) bool {
	var sA = d(A1, B1, B2)
	var sB = d(A2, B1, B2)
	var sP = d(B1, A1, A2)
	var sQ = d(B2, A1, A2)
	if sA*sB <= 0 && sP*sQ <= 0 {
		return true
	}
	return false
}
