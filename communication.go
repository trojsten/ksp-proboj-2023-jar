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
	data.WriteString(fmt.Sprintf("%f\n", w.Size))
	// 2 ja
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
	data.WriteString(fmt.Sprintf("%d\n", len(w.Players)))
	for _, p := range w.Players {
		if p.inReach(player.Position, player.RealStatsValues().Range) {
			data.WriteString(fmt.Sprintf("%d %f %f %f %f %d %f\n", aliveInt(p.Alive), p.X, p.Y, p.Angle, p.Tank.Radius(), p.Tank.TankId(), p.Health))
		}
	}

	// 4 bullets
	data.WriteString(fmt.Sprintf("%d\n", len(w.Bullets)))
	for _, b := range w.Bullets {
		if b.inReach(player.Position, player.RealStatsValues().Range) {
			data.WriteString(fmt.Sprintf("%f %f %f %f %d %f %f\n", b.X, b.Y, b.Vx, b.Vy, b.ShooterId, b.TTL, b.Damage))
		}
	}

	// 5 entities
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
	w.PlayerMovements = append(w.PlayerMovements, player.MoveTo(player.X+vx, player.Y+vy))
	player.Angle = angle

	if shoot == 1 {
		player.Fire()
	}

	if stat < StatNone || stat > StatReloadSpeed {
		return fmt.Errorf("unknown stat to upgrade: %d", stat)
	}
	if stat != StatNone {
		switch stat {
		case StatRange:
			if StatUpgradePrice[player.Stats.Range] <= player.Exp && len(RangeValues) > player.Stats.Range {
				player.Stats.Range += 1
				player.Exp -= StatUpgradePrice[player.Stats.Range]
			}
			break
		case StatSpeed:
			if StatUpgradePrice[player.Stats.Speed] <= player.Exp && len(SpeedValues) > player.Stats.Speed {
				player.Stats.Speed += 1
				player.Exp -= StatUpgradePrice[player.Stats.Speed]
			}
			break
		case StatBulletSpeed:
			if StatUpgradePrice[player.Stats.BulletSpeed] <= player.Exp && len(BulletSpeedValues) > player.Stats.BulletSpeed {
				player.Stats.BulletSpeed += 1
				player.Exp -= StatUpgradePrice[player.Stats.BulletSpeed]
			}
			break
		case StatBulletTTL:
			if StatUpgradePrice[player.Stats.BulletTTL] <= player.Exp && len(BulletTTLValues) > player.Stats.BulletTTL {
				player.Stats.BulletTTL += 1
				player.Exp -= StatUpgradePrice[player.Stats.BulletTTL]
			}
			break
		case StatBulletDamage:
			if StatUpgradePrice[player.Stats.BulletDamage] <= player.Exp && len(BulletDamageValues) > player.Stats.BulletDamage {
				player.Stats.BulletDamage += 1
				player.Exp -= StatUpgradePrice[player.Stats.BulletDamage]
			}
			break
		case StatHelathMax:
			if StatUpgradePrice[player.Stats.HealthMax] <= player.Exp && len(HealthMaxValues) > player.Stats.HealthMax {
				player.Stats.HealthMax += 1
				player.Exp -= StatUpgradePrice[player.Stats.HealthMax]
			}
			break
		case StatHealthRegeneration:
			if StatUpgradePrice[player.Stats.HealthRegeneration] <= player.Exp && len(HealthRegenerationValues) > player.Stats.HealthRegeneration {
				player.Stats.HealthRegeneration += 1
				player.Exp -= StatUpgradePrice[player.Stats.HealthRegeneration]
			}
			break
		case StatBodyDamage:
			if StatUpgradePrice[player.Stats.BodyDamage] <= player.Exp && len(BodyDamageValues) > player.Stats.BodyDamage {
				player.Stats.BodyDamage += 1
				player.Exp -= StatUpgradePrice[player.Stats.BodyDamage]
			}
			break
		case StatReloadSpeed:
			if StatUpgradePrice[player.Stats.ReloadSpeed] <= player.Exp && len(ReloadSpeedValues) > player.Stats.ReloadSpeed {
				player.Stats.ReloadSpeed += 1
				player.Exp -= StatUpgradePrice[player.Stats.ReloadSpeed]
			}
			break
		}
	}

	if newTankId != player.Tank.TankId() {
		// TODO: upgrade tank
	}

	return nil
}
