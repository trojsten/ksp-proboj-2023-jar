package main

import "math"

func intersect(A1 Position, A2 Position, radiusA float32, B1 Position, B2 Position, radiusB float32) bool {
	B2.X -= A2.X - A1.X
	B2.Y -= A2.Y - A1.Y
	if distanceSegmentToPoint(B1, B2, A1) <= radiusA+radiusB {
		return true
	}
	return false
}

// https://stackoverflow.com/a/1501725
func distanceSegmentToPoint(A1 Position, A2 Position, B Position) float32 {
	var l2 = SquaredDistance(A1, A2)

	if l2 == 0.0 {
		return Distance(B, A1)
	}
	var t = float32(math.Max(0, math.Min(1, float64(DotProduct(B, A1, A2)/l2))))
	var projectionX = A1.X + t*(A2.X-A1.X)
	var projectionY = A1.Y + t*(A2.Y-A1.Y)
	return Distance(B, Position{projectionX, projectionY})
}

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

func Distance(A Position, B Position) float32 {
	var d1 = A.X - B.X
	var d2 = A.Y - B.Y

	return float32(math.Sqrt(float64(d1*d1 + d2*d2)))
}

func SquaredDistance(A Position, B Position) float32 {
	var d1 = A.X - B.X
	var d2 = A.Y - B.Y

	return d1*d1 + d2*d2
}

func Dot(Px float32, Py float32, Vx float32, Vy float32) float32 {
	return Vx*Px + Vy*Py
}
