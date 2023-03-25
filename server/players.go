package main

import (
	"encoding/json"
	"fmt"
)

type Player struct {
	Position
	Statistics
	Id              int
	Name            string
	Alive           bool
	Health          float32
	Exp             int
	Level           int
	LevelsLeft      int
	TankUpdatesLeft int
	Angle           float32
	Stats           Stats
	Tank            Tank
	World           *World
	ReloadCooldown  int
	LifesLeft       int
	Score           int
}

func (p *Player) MarshalJSON() ([]byte, error) {
	return json.Marshal(struct {
		X          float32 `json:"x"`
		Y          float32 `json:"y"`
		Angle      float32 `json:"angle"`
		Alive      bool    `json:"alive"`
		Id         int     `json:"id"`
		Name       string  `json:"name"`
		TankId     int     `json:"tank_id"`
		TankRadius float32 `json:"tank_radius"`
		Range      float32 `json:"range"`
		Health     float32 `json:"health"`
		MaxHealth  float32 `json:"max_health"`
		Score      int     `json:"score"`
		Stats      Stats   `json:"stats"`
	}{
		X:          p.X,
		Y:          p.Y,
		Angle:      p.Angle,
		Alive:      p.Alive,
		Id:         p.Id,
		Name:       p.Name,
		TankId:     p.Tank.TankId(),
		TankRadius: p.Tank.Radius(),
		Range:      p.RealStatsValues().Range,
		Health:     p.Health,
		MaxHealth:  p.RealStatsValues().HealthMax,
		Score:      p.Score,
		Stats:      p.Stats,
	})
}

func (w *World) NewPlayer(name string) Player {
	return Player{Name: name, Tank: BasicTank{}, Alive: true, World: w, LifesLeft: MaxRespawn, Health: HealthMaxValues[0]}
}

func (p *Player) RealStatsValues() StatsValues {
	var tankStats = p.Tank.StatsValues()

	return StatsValues{
		RangeValues[p.Stats.Range] + tankStats.Range,
		SpeedValues[p.Stats.Speed] + tankStats.Speed,
		BulletSpeedValues[p.Stats.BulletSpeed] + tankStats.BulletSpeed,
		BulletTTLValues[p.Stats.BulletTTL] + tankStats.BulletTTL,
		BulletDamageValues[p.Stats.BulletDamage] + tankStats.BulletDamage,
		HealthMaxValues[p.Stats.HealthMax] + tankStats.HealthMax,
		HealthRegenerationValues[p.Stats.HealthRegeneration] + tankStats.HealthRegeneration,
		BodyDamageValues[p.Stats.BodyDamage] + tankStats.BodyDamage,
		ReloadSpeedValues[p.Stats.ReloadSpeed] + tankStats.ReloadSpeed,
	}
	// TODO: možno reload speed reprezentovať inak, lebo takto to môže klesnúť pod nulu
}

func (p *Player) MoveTo(x, y float32) PlayerMovement {
	var movement = PlayerMovement{Position{X: x, Y: y}, p}
	// p.X = InRange(x, -p.World.Size, p.World.Size)
	// p.Y = InRange(y, -p.World.Size, p.World.Size)
	return movement
}

func (p *Player) Fire(playerMovement PlayerMovement, angle2 float32, target Target) (float32, float32) {
	if p.ReloadCooldown > 0 {
		p.World.Runner.Log(fmt.Sprintf("(%s) ignoring shoot: reload cooldown", p.Name))
		return 0, 0
	}

	p.ReloadCooldown = p.RealStatsValues().ReloadSpeed
	return p.Tank.Fire(p, playerMovement, angle2, target)
}

func (p *Player) Tick() {
	if !p.Alive {
		return
	}

	if _, exists := p.Statistics.TimeByTank[p.Tank.TankId()]; exists {
		p.Statistics.TimeByTank[p.Tank.TankId()] += 1
	} else {
		p.Statistics.TimeByTank[p.Tank.TankId()] = 1
	}

	if p.ReloadCooldown > 0 {
		p.ReloadCooldown--
		p.Statistics.TimeInCooldown += 1
	} else {
		p.Statistics.TimeNotInCooldown += 1
	}

	if p.X != InRange(p.X, p.World.MinX, p.World.MaxX) ||
		p.Y != InRange(p.Y, p.World.MinY, p.World.MaxY) {
		p.Health -= PlayerOutOfWorldHealth
	}

	if p.Health < 0 {
		p.Alive = false
		p.World.Runner.Log(fmt.Sprintf("(%s) player died", p.Name))
		if p.LifesLeft > 0 {
			p.RespawnPlayer()
			p.World.Runner.Log(fmt.Sprintf("(%s) player respawned. Lifes left: %d", p.Name, p.LifesLeft))
		} else {
			p.World.DiedOrder = append(p.World.DiedOrder, *p)
		}
	}

	p.Health = Min(p.RealStatsValues().HealthMax, p.Health+p.RealStatsValues().HealthRegeneration)

	for p.Level < len(LevelUpdateExp) && p.Exp > LevelUpdateExp[p.Level] {
		p.Level++
		p.LevelsLeft++
		p.World.Runner.Log(fmt.Sprintf("(%s) player level updated. New level: %d", p.Name, p.Level))
		if p.Level%TankLevelUpdateFreq == 0 {
			p.TankUpdatesLeft++
			p.World.Runner.Log(fmt.Sprintf("(%s) player tank level updated. New tank level", p.Name))
		}
	}
}

func (p *Player) RespawnPlayer() {
	p.LifesLeft--
	p.World.SpawnObject(&p.Position)
	p.Tank = BasicTank{}
	p.Alive = true
	p.Stats = Stats{}
	p.Level /= 2
	p.LevelsLeft = p.Level
	if p.Level > 0 {
		p.Exp = LevelUpdateExp[p.Level-1]
	} else {
		p.Exp = 0
	}
	p.TankUpdatesLeft = p.Level / TankLevelUpdateFreq
	p.ReloadCooldown = 0
	p.Health = p.RealStatsValues().HealthMax
}

func (p *Player) UpdateTank(newTank Tank) {
	if p.TankUpdatesLeft > 0 {
		p.World.Runner.Log(fmt.Sprintf("(%s) player tank updated. New tank id: %d", p.Name, newTank.TankId()))
		p.Tank = newTank
		p.TankUpdatesLeft--
	}
}

func (p *Player) ReachablePlayers() []Player {
	var res []Player
	for _, player := range p.World.AlivePlayers() {
		if p.Reachable(player.Position, p.RealStatsValues().Range) {
			res = append(res, *player)
		}
	}
	return res
}

func (p *Player) ReachableEntities() []Entity {
	var res []Entity
	for _, entity := range p.World.Entities {
		if p.Reachable(entity.Position, p.RealStatsValues().Range) {
			res = append(res, entity)
		}
	}
	return res
}

func (p *Player) AddExp(Exp int, reason Reason) {
	p.Exp += Exp
	p.Score += Exp
	if _, exists := p.Statistics.ScoreByReason[reason]; exists {
		p.Statistics.ScoreByReason[reason] += Exp
	} else {
		p.Statistics.ScoreByReason[reason] = Exp
	}
}

func (p *Player) ReachableVisibleBullets() []Bullet {
	var res []Bullet
	for _, bullet := range p.World.Bullets {
		if bullet.Visible && p.Reachable(bullet.Position, p.RealStatsValues().Range) {
			res = append(res, bullet)
		}
	}
	return res
}

type PlayerMovement struct {
	NewPosition Position
	Player      *Player
}

func (pm PlayerMovement) speed() float32 {
	return pm.NewPosition.Distance(pm.Player.Position)
}

func (pm PlayerMovement) apply() {
	pm.Player.Position = pm.NewPosition
}
