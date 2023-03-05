package main

import (
	"github.com/trojsten/ksp-proboj/libproboj"
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
