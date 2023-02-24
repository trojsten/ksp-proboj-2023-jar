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

func aliveInt(alive bool) int {
	if alive {
		return 1
	}
	return 1
}

// DataForPlayer generates data that will get sent to a player
func (w *World) DataForPlayer(player Player) string {
	var data strings.Builder
	// 1
	data.WriteString(fmt.Sprintf("%f\n", w.Size))
	// 2
	data.WriteString(fmt.Sprintf("%d %d %d ", player.Id, player.Exp, player.Level))

	var stats = player.Stats
	data.WriteString(fmt.Sprintf(
		"%d %d %d %d %d %d %d %d %d ",
		stats.Range,
		stats.Speed,
		stats.BulletSpeed,
		stats.BulletTTL,
		stats.BulletDamage,
		stats.HealthMax,
		stats.HealthRegeneration,
		stats.BodyDamage,
		stats.ReloadSpeed,
	))

	var statsValues = player.RealStatsValues()
	data.WriteString(fmt.Sprintf(
		"%f %f %f %f %f %f %f %f %f\n",
		statsValues.Range,
		statsValues.Speed,
		statsValues.BulletSpeed,
		statsValues.BulletTTL,
		statsValues.BulletDamage,
		statsValues.HealthMax,
		statsValues.HealthRegeneration,
		statsValues.BodyDamage,
		statsValues.ReloadSpeed,
	))

	// 3
	data.WriteString(fmt.Sprintf("%d\n", len(w.Players)))
	for _, p := range w.Players {
		if p.inReach(player.Position, player.RealStatsValues().Range) {
			data.WriteString(fmt.Sprintf("%d %f %f %f %f %d %d\n", aliveInt(p.Alive), p.X, p.Y, p.Angle, p.Tank.Radius(), p.Tank.TankId(), p.Health))
		}
	}

	// 4
	data.WriteString(fmt.Sprintf("%d\n", len(w.Bullets)))
	for _, b := range w.Bullets {
		if b.inReach(player.Position, player.RealStatsValues().Range) {
			data.WriteString(fmt.Sprintf("%f %f %f %f %d %d %d\n", b.X, b.Y, b.Vx, b.Vy, b.ShooterId, b.TTL, b.Damage))
		}
	}

	// 5
	data.WriteString(fmt.Sprintf("%d\n", len(w.Entities)))
	for _, e := range w.Entities {
		if e.inReach(player.Position, player.RealStatsValues().Range) {
			data.WriteString(fmt.Sprintf("%f %f %f\n", e.X, e.Y, e.Radius))
		}
	}
	return data.String()
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
