package main

import (
	"encoding/json"
	"fmt"
)

type Player struct {
	Position
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
	})
}

func (w *World) NewPlayer(name string) Player {
	return Player{Name: name, Tank: BasicTank{}, Alive: true, World: w, LifesLeft: MaxRespawn}
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
	var movement = PlayerMovement{p.Position, p}
	// p.X = InRange(x, -p.World.Size, p.World.Size)
	// p.Y = InRange(y, -p.World.Size, p.World.Size)
	p.X = x
	p.Y = y
	return movement
}

func (p *Player) Fire(playerMovement PlayerMovement) {
	if p.ReloadCooldown > 0 {
		p.World.Runner.Log(fmt.Sprintf("ignoring shoot for %s: reload cooldown", p.Name))
		return
	}

	p.Tank.Fire(p, playerMovement)
	p.ReloadCooldown = p.RealStatsValues().ReloadSpeed
}

func (p *Player) Tick() {
	if !p.Alive {
		return
	}

	if p.ReloadCooldown > 0 {
		p.ReloadCooldown--
	}

	if p.X != InRange(p.X, p.World.MinX, p.World.MaxX) ||
		p.Y != InRange(p.Y, p.World.MinY, p.World.MaxY) {
		p.Health -= PlayerOutOfWorldHealth
	}

	if p.Health < 0 {
		p.Alive = false
		if p.LifesLeft > 0 {
			p.RespawnPlayer()
		}
	}

	p.Health = Min(p.RealStatsValues().HealthMax, p.Health+p.RealStatsValues().HealthRegeneration)

	for p.Level < len(LevelUpdateExp) && p.Exp > LevelUpdateExp[p.Level] {
		p.Level++
		p.LevelsLeft++
		if p.Level%TankLevelUpdateFreq == 0 {
			p.TankUpdatesLeft++
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

func (p *Player) ReachableBullets() []Bullet {
	var res []Bullet
	for _, bullet := range p.World.Bullets {
		if p.Reachable(bullet.Position, p.RealStatsValues().Range) {
			res = append(res, bullet)
		}
	}
	return res
}

type PlayerMovement struct {
	OldPosition Position
	Player      *Player
}

func (pm PlayerMovement) speed() float32 {
	return pm.OldPosition.Distance(pm.Player.Position)
}
