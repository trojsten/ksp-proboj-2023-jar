package main

type Entity struct {
	Position
	Radius float32
}

type EntityMovement struct {
	OldPosition Position
	Entity      *Entity
}
