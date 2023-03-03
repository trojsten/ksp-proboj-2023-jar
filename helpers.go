package main

import "math"

func d(A Position, B Position, C Position) float32 {
	return A.X*(B.Y-C.Y) + A.Y*(C.X-B.X) + B.X*C.Y - B.Y*C.X
}

// NaiveIntersect https://dai.fmph.uniba.sk/upload/e/ee/Cg1_Prieniky.pdf
// druhý spôsob
func NaiveIntersect(A1 Position, A2 Position, radiusA float32, B1 Position, B2 Position, radiusB float32) bool {
	var sA = d(A1, B1, B2)
	var sB = d(A2, B1, B2)
	var sP = d(B1, A1, A2)
	var sQ = d(B2, A1, A2)
	if sA*sB <= 0 && sP*sQ <= 0 {
		return true
	}
	return false
}

func intersect(A1 Position, A2 Position, radiusA float32, B1 Position, B2 Position, radiusB float32) bool {
	B2.X -= A2.X - A1.X
	B2.Y -= A2.Y - A1.Y
	if distanceSegmentToPoint(B1, B2, A1) <= radiusA+radiusB {
		return true
	}
	return false
}

// https://stackoverflow.com/a/4448097
func otherDistanceSegmentToPoint(A1 Position, A2 Position, B Position) float32 {
	var dist = CrossProduct(A1, A2, B) / Distance(A1, A2)
	var dot1 = DotProduct(A1, A2, B)
	if dot1 > 0 {
		return Distance(A2, B)
	}

	var dot2 = DotProduct(A2, A1, B)
	if dot2 > 0 {
		return Distance(A1, B)
	}
	return float32(math.Abs(float64(dist)))
}

func distanceSegmentToPoint(A1 Position, A2 Position, B Position) float32 {
	var l2 = SquaredDistance(A1, A2)

	if l2 == 0.0 {
		return Distance(B, A1)
	}
	var t = float32(math.Max(0, math.Min(1, float64(BetterDotProduct(B, A1, A2)/l2))))
	var projectionX = A1.X + t*(A2.X-A1.X)
	var projectionY = A1.Y + t*(A2.Y-A1.Y)
	return Distance(B, Position{projectionX, projectionY})
}

func BetterDotProduct(A Position, B Position, C Position) float32 {
	var AB = Position{
		X: A.X - B.X,
		Y: A.Y - B.Y,
	}
	var BC = Position{
		X: C.X - B.X,
		Y: C.Y - B.Y,
	}
	return AB.X*BC.X + AB.Y*BC.Y
}

// DotProduct Compute the dot product AB . BC
func DotProduct(A Position, B Position, C Position) float32 {
	var AB = Position{
		X: B.X - A.X,
		Y: B.Y - A.Y,
	}
	var BC = Position{
		X: C.X - B.X,
		Y: C.Y - B.Y,
	}
	return AB.X*BC.X + AB.Y*BC.Y
}

// CrossProduct Compute the cross product AB x AC
func CrossProduct(A Position, B Position, C Position) float32 {
	var AB = Position{
		X: B.X - A.X,
		Y: B.Y - A.Y,
	}
	var AC = Position{
		X: C.X - A.X,
		Y: C.Y - A.Y,
	}
	return AB.X*AC.Y - AB.Y*AC.X
}

// Distance Compute the distance from A to B
func Distance(A Position, B Position) float32 {
	var d1 = A.X - B.X
	var d2 = A.Y - B.Y

	return float32(math.Sqrt(float64(d1*d1 + d2*d2)))
}

// Distance Compute the distance from A to B
func SquaredDistance(A Position, B Position) float32 {
	var d1 = A.X - B.X
	var d2 = A.Y - B.Y

	return d1*d1 + d2*d2
}
