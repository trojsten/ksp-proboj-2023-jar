package main

import (
	"fmt"
	"math"
	"strings"
)

// DataForPlayer generates data that will get sent to a player
func (w *World) DataForPlayer(player Player) string {
	var data strings.Builder
	// 1 svet
	data.WriteString(fmt.Sprintf("%f %f %f %f\n", w.MinX, w.MaxX, w.MinY, w.MaxY))
	// 2 ja
	data.WriteString(fmt.Sprintf(
		"%d %d %d %d %d %d %d\n",
		player.Id,
		player.Exp,
		player.Level,
		player.LevelsLeft,
		player.TankUpdatesLeft,
		player.ReloadCooldown,
		player.LifesLeft,
	))

	var stats = player.Stats
	data.WriteString(fmt.Sprintf(
		"%d %d %d %d %d %d %d %d %d\n",
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
		"%f %f %f %f %f %f %f %f %d\n",
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

	// 3 players
	var reachablePlayers = player.ReachablePlayers()
	data.WriteString(fmt.Sprintf("%d\n", len(reachablePlayers)))
	for _, p := range reachablePlayers {
		data.WriteString(fmt.Sprintf(
			"%d %d %f %f %f %f %d %f\n",
			p.Id,
			aliveInt(p.Alive),
			p.X,
			p.Y,
			p.Angle,
			p.Tank.Radius(),
			p.Tank.TankId(),
			p.Health,
		))
	}

	// 4 bullets
	var reachableBullets = player.ReachableVisibleBullets()
	data.WriteString(fmt.Sprintf("%d\n", len(reachableBullets)))
	for _, b := range reachableBullets {
		data.WriteString(fmt.Sprintf(
			"%f %f %f %f %d %f %f\n",
			b.X,
			b.Y,
			b.Vx,
			b.Vy,
			b.ShooterId,
			b.TTL,
			b.Damage,
		))
	}

	// 5 entities
	var reachableEntities = player.ReachableEntities()
	data.WriteString(fmt.Sprintf("%d\n", len(reachableEntities)))
	for _, e := range reachableEntities {
		data.WriteString(fmt.Sprintf("%f %f %f %f\n", e.X, e.Y, e.Radius, e.Health))
	}
	return data.String()
}

// ParseResponse parses the player's response and updates game state
// response format is `vx vy angle shoot? statsDiff... newTankId`
func (w *World) ParseResponse(response string, player *Player) error {
	var vx, vy, angle float32
	var shoot, newTankId int
	var stat Stat
	_, err := fmt.Sscanf(response, "%f %f %f %d %d %d", &vx, &vy, &angle, &shoot, &stat, &newTankId)
	if err != nil {
		return fmt.Errorf("sscanf failed: %w", err)
	}

	// check if vx/vy is Inf/-Inf/NaN
	if math.IsInf(float64(vx), 1) || math.IsInf(float64(vx), -1) || math.IsNaN(float64(vx)) {
		w.Runner.Log(fmt.Sprintf("(%s) invalid vx: %f", player.Name, vx))
		vx = 0
	}
	if math.IsInf(float64(vy), 1) || math.IsInf(float64(vy), -1) || math.IsNaN(float64(vy)) {
		w.Runner.Log(fmt.Sprintf("(%s) invalid vy: %f", player.Name, vy))
		vy = 0
	}
	// Limit vx, vy length to speed stat
	dist := math.Sqrt(math.Pow(float64(vx), 2) + math.Pow(float64(vy), 2))
	maxSpeed := float64(player.RealStatsValues().Speed)
	if dist > maxSpeed && dist > 1e-10 {
		vx = float32(float64(vx) / dist * maxSpeed)
		vy = float32(float64(vy) / dist * maxSpeed)
	}
	playerMovement := player.MoveTo(player.X+vx, player.Y+vy)
	w.PlayerMovements = append(w.PlayerMovements, playerMovement)
	player.Angle = angle

	// Shoot
	var knockX, knockY float32 = 0, 0
	if shoot == 1 {
		knockX, knockY = player.Fire(playerMovement)
	}

	playerMovement.apply()
	player.X += knockX
	player.Y += knockY

	// Upgrade stats
	if stat.IsValid() {
		if stat != StatNone {
			err := player.UpgradeStat(stat)
			if err != nil {
				w.Runner.Log(fmt.Sprintf("(%s) ignoring stat upgrade: %s", player.Name, err.Error()))
			}
		}
	} else {
		w.Runner.Log(fmt.Sprintf("(%s) ignoring stat upgrade: unknown stat %d", player.Name, stat))
	}

	if newTankId != player.Tank.TankId() {
		var b, tank = CanUpdateTank(player.Tank, newTankId)
		if b {
			player.UpdateTank(tank)
		}
	}

	return nil
}
