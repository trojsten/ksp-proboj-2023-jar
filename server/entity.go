package main

import "math/rand"

type Entity struct {
	Position `json:"position"`
	Radius   float32 `json:"radius"`
}

func (w *World) NewEntity() Entity {
	return Entity{Radius: rand.Float32() * MaxEntityRadius+MinEntityRadius}
}
