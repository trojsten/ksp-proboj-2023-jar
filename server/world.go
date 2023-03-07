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
	MinX            float32          `json:"MinX"`
	MaxX            float32          `json:"MaxX"`
	MinY            float32          `json:"MinY"`
	MaxY            float32          `json:"MaxY"`
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
	p.X = rand.Float32()*(w.MaxX-w.MinX) + w.MinX
	p.Y = rand.Float32()*(w.MaxY-w.MinY) + w.MinY
}

func (w *World) SpawnEntity() {
	var entity = w.NewEntity()
	w.SpawnObject(&entity.Position)
	w.Entities = append(w.Entities, entity)
}

// AlivePlayers returns a list of currently alive players
func (w *World) AlivePlayers() (players []*Player) {
	for i, player := range w.Players {
		if player.Alive {
			players = append(players, &w.Players[i])
		}
	}
	return
}
