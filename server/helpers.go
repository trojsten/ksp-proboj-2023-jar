package main

// TODO: move to geometry.go
func DotProduct(A Position, B Position, C Position) float32 {
	var AB = Position{
		X: A.X - B.X,
		Y: A.Y - B.Y,
	}
	var CB = Position{
		X: C.X - B.X,
		Y: C.Y - B.Y,
	}
	return AB.X*CB.X + AB.Y*CB.Y
}

// TODO: move to geometry.go
func Dot(Px float32, Py float32, Vx float32, Vy float32) float32 {
	return Vx*Px + Vy*Py
}
