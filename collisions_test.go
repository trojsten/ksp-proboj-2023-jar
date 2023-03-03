package main

import (
	"math"
	"testing"
)

func TestDistance(t *testing.T) {
	var distance = Distance(Position{X: 0, Y: 0}, Position{X: 0, Y: 0})
	if distance != 0 {
		t.Fatalf(`Distance should be 0"`)
	}
	distance = Distance(Position{X: 0, Y: 0}, Position{X: 1, Y: 0})
	if distance != 1 {
		t.Fatalf(`Distance should be 1"`)
	}
	distance = Distance(Position{X: 0, Y: 0}, Position{X: 1, Y: 1})
	if distance != float32(math.Sqrt(2)) {
		t.Fatalf(`Distance should be \sqrt(2)"`)
	}
}

func TestDotProduct(t *testing.T) {
	var result = DotProduct(Position{X: 0, Y: 0}, Position{X: 0, Y: 0}, Position{X: 0, Y: 0})
	if result != 0 {
		t.Fatalf(`Dot product should be 0"`)
	}
	result = DotProduct(Position{X: 1, Y: 0}, Position{X: 0, Y: 0}, Position{X: 0, Y: 1})
	if result != 0 {
		t.Fatalf(`Dot product should be 0"`)
	}
	result = DotProduct(Position{X: 1, Y: 0}, Position{X: 0, Y: 0}, Position{X: 1, Y: 0})
	if result != -1 {
		t.Fatalf(`Dot product should be -1, is %f"`, result)
	}
	result = DotProduct(Position{X: 2, Y: 1}, Position{X: 1, Y: 1}, Position{X: 2, Y: 2})
	if result != -1 {
		t.Fatalf(`Dot product should be -1, is %f"`, result)
	}
}

func TestCrossProduct(t *testing.T) {
	var result = CrossProduct(Position{X: 0, Y: 0}, Position{X: 0, Y: 0}, Position{X: 0, Y: 0})
	if result != 0 {
		t.Fatalf(`Cross product should be 0, is %f"`, result)
	}
	result = CrossProduct(Position{X: -1, Y: -2}, Position{X: 0, Y: 0}, Position{X: 3, Y: 4})
	if result != -2 {
		t.Fatalf(`Cross product should be -2, is %f"`, result)
	}
	result = CrossProduct(Position{X: 1, Y: 1}, Position{X: 0, Y: 0}, Position{X: 1, Y: 1})
	if result != 0 {
		t.Fatalf(`Cross product should be 0, is %f"`, result)
	}
	result = CrossProduct(Position{X: 2, Y: 1}, Position{X: 1, Y: 1}, Position{X: 4, Y: 5})
	if result != -4 {
		t.Fatalf(`Cross product should be 4, is %f"`, result)
	}
}

func TestIntersect1(t *testing.T) {
	var intersects = intersect(Position{X: 0, Y: 0}, Position{X: 0, Y: 0}, 1,
		Position{X: 1, Y: 0}, Position{X: 1, Y: 0}, 1)
	if !intersects {
		t.Fatalf(`Points intersects!`)
	}
}

func TestIntersect2(t *testing.T) {
	var intersects = intersect(Position{X: 0, Y: 0}, Position{X: 0, Y: 0}, 1,
		Position{X: 10, Y: 10}, Position{X: 10, Y: 10}, 1)
	if intersects {
		t.Fatalf(`Points NOT intersects!`)
	}
}

func TestIntersect3(t *testing.T) {
	var intersects = intersect(Position{X: 0, Y: 0}, Position{X: 10, Y: 0}, 1,
		Position{X: 5, Y: 0}, Position{X: 5, Y: 0}, 1)
	if !intersects {
		t.Fatalf(`Points intersects!`)
	}
}

func TestIntersect4(t *testing.T) {
	var intersects = intersect(Position{X: 0, Y: 0}, Position{X: 10, Y: 0}, 1,
		Position{X: 5, Y: 0}, Position{X: 5, Y: 0}, 1)
	if !intersects {
		t.Fatalf(`Points intersects!`)
	}
}
