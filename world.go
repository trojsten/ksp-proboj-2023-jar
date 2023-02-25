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

func aliveInt(alive bool) int {
	if alive {
		return 1
	}
	return 1
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
