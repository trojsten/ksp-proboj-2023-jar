package main

import (
	"fmt"
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
	var x = rand.Float32()*(w.MaxX-w.MinX) + w.MinX
	var y = rand.Float32()*(w.MaxY-w.MinY) + w.MinY
	var dist = w.NearestPlayerDistance(Position{X: x, Y: y})
	for i := 0; i < SpawnIterations; i++ {
		var x2 = rand.Float32()*(w.MaxX-w.MinX) + w.MinX
		var y2 = rand.Float32()*(w.MaxY-w.MinY) + w.MinY
		var dist2 = w.NearestPlayerDistance(Position{X: x2, Y: y2})
		if dist > dist2 {
			x = x2
			y = y2
		}
	}
	p.X = x
	p.Y = y
}

func (w *World) NearestPlayerDistance(p Position) float32 {
	var minDistance = float32(math.Inf(1))
	for _, player := range w.Players {
		minDistance = Min(minDistance, player.Distance(p))
	}
	return minDistance
}

func (w *World) SpawnEntity() {
	var entity = w.NewEntity()
	w.SpawnObject(&entity.Position)
	w.Runner.Log(fmt.Sprintf("spawned entity on (%f, %f)", entity.Position.X, entity.Position.Y))
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

func (w *World) CalculateCG() Position {
	var x, y float32
	for _, player := range w.Players {
		x += player.X
		y += player.Y
	}
	return Position{
		X: x / float32(len(w.Players)),
		Y: y / float32(len(w.Players)),
	}
}

func (w *World) Shrink() {
	if w.TickNumber > ShrinkWorldAfter {
		if (w.MaxX-w.MinX) > MinWorldSize || (w.MaxY-w.MinY) > MinWorldSize {
			var CG = w.CalculateCG()
			var shrinkX = (w.MaxX - w.MinX) * WorldSizeShrink
			var shrinkY = (w.MaxY - w.MinY) * WorldSizeShrink
			w.MinX += (CG.X - w.MinX) / shrinkX
			w.MaxX -= (w.MaxX - CG.X) / shrinkX
			w.MinY += (CG.Y - w.MinY) / shrinkY
			w.MaxY -= (w.MaxY - CG.X) / shrinkY
		}
	}
}
