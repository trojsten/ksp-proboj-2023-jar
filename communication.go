package main

import (
	"fmt"
	"math"
	"strings"
)

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

// ParseResponse parses the player's response and updates game state
// response format is `vx vy angle shoot? statsDiff... newTankId`
func (w *World) ParseResponse(response string, player *Player) error {
	var vx, vy, angle float32
	var shoot, newTankId int
	var stat Stat
	_, err := fmt.Sscanf(response, "%f %f %f %d %d %d", vx, vy, angle, shoot, stat, newTankId)
	if err != nil {
		return fmt.Errorf("sscanf failed: %w", err)
	}

	// Limit vx, vy length to speed stat
	dist := math.Sqrt(math.Pow(float64(vx), 2) + math.Pow(float64(vy), 2))
	maxSpeed := float64(player.RealStatsValues().Speed)
	if dist > maxSpeed {
		vx = float32(float64(vx) / dist * maxSpeed)
		vy = float32(float64(vy) / dist * maxSpeed)
	}
	player.MoveTo(player.X+vx, player.Y+vy)
	player.Angle = angle // TODO: limit rotation?

	if shoot == 1 {
		player.Fire()
	}

	if stat < StatNone || stat > StatReloadSpeed {
		return fmt.Errorf("unknown stat to upgrade: %d", stat)
	}
	if stat != StatNone {
		// TODO: upgrade the given stat
	}

	if newTankId != player.Tank.TankId() {
		// TODO: upgrade tank
	}

	return nil
}
