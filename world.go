package main

import (
	"fmt"
	"github.com/trojsten/ksp-proboj/libproboj"
	"math"
	"strings"
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
	var data strings.Builder
	data.WriteString(fmt.Sprintf("%d\n", len(w.Players)))
	for _, p := range w.Players {
		if p.inReach(player.Position, player.StatsValues().Range) {
			// TODO tank id, alive
			data.WriteString(fmt.Sprintf("%d %f %f %f %f %d %d\n", p.Alive, p.Position.X, p.Position.Y, p.Angle, p.Tank.Radius(), 0, p.Health))
		}
	}
	for _, b := range w.Bullets {
		if b.inReach(player.Position, player.StatsValues().Range) {
			// TODO add
		}
	}
	for _, e := range w.Entities {
		if e.inReach(player.Position, player.StatsValues().Range) {
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
