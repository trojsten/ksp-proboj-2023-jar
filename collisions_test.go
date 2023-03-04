package main

import (
	"testing"
)

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
	var intersects = intersect(Position{X: 0, Y: 0}, Position{X: 1, Y: 0}, 1,
		Position{X: 1, Y: 0}, Position{X: 0, Y: 0}, 1)
	if !intersects {
		t.Fatalf(`Points intersects!`)
	}
}

func TestIntersect5(t *testing.T) {
	var intersects = intersect(Position{X: 0, Y: 0}, Position{X: 1, Y: 0}, 0,
		Position{X: 1, Y: 0}, Position{X: 0, Y: 0}, 0)
	if !intersects {
		t.Fatalf(`Points intersects!`)
	}
}

func TestIntersect6(t *testing.T) {
	var intersects = intersect(Position{X: 0, Y: 0}, Position{X: 1, Y: 0}, 1,
		Position{X: 1, Y: 1}, Position{X: 0, Y: 1}, 1)
	if !intersects {
		t.Fatalf(`Points intersects!`)
	}
}

func TestIntersect7(t *testing.T) {
	var intersects = intersect(Position{X: 0, Y: 0}, Position{X: 1, Y: 0}, 0.5,
		Position{X: 1, Y: 1}, Position{X: 0, Y: 1}, 0.5)
	if !intersects {
		t.Fatalf(`Points intersects!`)
	}
}

func TestIntersect8(t *testing.T) {
	var intersects = intersect(Position{X: 0, Y: 0}, Position{X: 1, Y: 0}, 0.5,
		Position{X: 1, Y: 1}, Position{X: 0, Y: 1}, 0.49)
	if intersects {
		t.Fatalf(`Points NOT intersects!`)
	}
}

func TestIntersect9(t *testing.T) {
	var intersects = intersect(Position{X: 0, Y: 0}, Position{X: 0, Y: 100}, 1,
		Position{X: -100, Y: 100}, Position{X: 100, Y: 100}, 1)
	if intersects {
		t.Fatalf(`Points NOT intersects!`)
	}
}

func TestIntersect10(t *testing.T) {
	var intersects = intersect(Position{X: 0, Y: 0}, Position{X: 0, Y: 100}, 1,
		Position{X: -100, Y: 0}, Position{X: 100, Y: 0}, 1)
	if intersects {
		t.Fatalf(`Points NOT intersects!`)
	}
}
