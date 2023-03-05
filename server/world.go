package main

import (
	"github.com/trojsten/ksp-proboj/libproboj"
	"math"
	"math/rand"
)

type World struct {
	Runner          libproboj.Runner
	Players         []Player         `json:"players"`
	PlayerMovements []PlayerMovement `json:"-"`
	Bullets         []Bullet         `json:"bullets"`
	BulletMovements []BulletMovement `json:"-"`
	Entities        []Entity         `json:"entities"`
	Size            float32          `json:"size"`
	TickNumber      int              `json:"tick_number"`
	BulletNumber    int              `json:"-"`
}

func aliveInt(alive bool) int {
	if alive {
		return 1
	}
	return 0
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
	X float32 `json:"x"`
	Y float32 `json:"y"`
}

func (p Position) inReach(p2 Position, distance float32) bool {
	return math.Pow(float64(p.X-p2.X), 2)+math.Pow(float64(p.Y-p2.Y), 2) < math.Pow(float64(distance), 2)
}

func (w *World) SpawnObject(p *Position) {
	// TODO check, ci nie som blizko niekoho
	p.X = rand.Float32()*2*w.Size - w.Size
	p.Y = rand.Float32()*2*w.Size - w.Size
}

func (w *World) SpawnEntity() {
	var entity = w.NewEntity()
	w.SpawnObject(&entity.Position)
	w.Entities = append(w.Entities, entity)
}
