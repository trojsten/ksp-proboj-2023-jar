package main

import "math/rand"

type Entity struct {
	Position
	Radius float32
}

func (w *World) NewEntity() Entity {
	return Entity{Radius: rand.Float32() * MaxEntityRadius}
}

type EntityMovement struct {
	OldPosition Position
	Entity      *Entity
}
