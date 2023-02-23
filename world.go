package main

import "github.com/trojsten/ksp-proboj/libproboj"

type World struct {
	Runner     libproboj.Runner
	Players    []Player
	Bullets    []Bullet
	Entities   []Entity
	Size       float32
	TickNumber int
}

// DataForPlayer generates data that will get sent to a player
func (w *World) DataForPlayer(player Player) string {
	// TODO
	return ""
}

// Running returns whether the game is still running
func (w *World) Running() bool {
	// TODO
	return true
}
