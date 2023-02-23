package main

import (
	"github.com/trojsten/ksp-proboj/libproboj"
	"math"
)

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
	for _, p := range w.Players {
		if p.inReach(player.Position, player.getRange()) {
			// TODO add
		}
	}
	for _, b := range w.Bullets {
		if b.inReach(player.Position, player.getRange()) {
			// TODO add
		}
	}
	for _, e := range w.Entities {
		if e.inReach(player.Position, player.getRange()) {
			// TODO add
		}
	}
	return ""
}

// Running returns whether the game is still running
func (w *World) Running() bool {
	alivePlayers := 0
	for _, player := range w.Players {
		if player.Alive {
			alivePlayers++
		}
	}
	return alivePlayers >= 2
}

type Position struct {
	X float32
	Y float32
}

func (p Position) inReach(p2 Position, distance float32) bool {
	return math.Pow(float64(p.X-p2.X), 2)+math.Pow(float64(p.Y-p2.Y), 2) < math.Pow(float64(distance), 2)
}
