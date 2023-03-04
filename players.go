package main

import (
	"encoding/json"
	"fmt"
	"math"
)

type Stat int

const (
	StatRange Stat = iota
	StatSpeed
	StatBulletSpeed
	StatBulletTTL
	StatBulletDamage
	StatHealthMax
	StatHealthRegeneration
	StatBodyDamage
	StatReloadSpeed
	StatNone
)

type StatsValues struct {
	Range              float32
	Speed              float32
	BulletSpeed        float32
	BulletTTL          float32
	BulletDamage       float32
	HealthMax          float32
	HealthRegeneration float32
	BodyDamage         float32
	ReloadSpeed        int
}

type Stats struct {
	Range              int
	Speed              int
	BulletSpeed        int
	BulletTTL          int
	BulletDamage       int
	HealthMax          int
	HealthRegeneration int
	BodyDamage         int
	ReloadSpeed        int
}

var RangeValues = []float32{1, 2, 3, 4}
var SpeedValues = []float32{1, 2, 3, 4}
var BulletSpeedValues = []float32{1, 2, 3, 4}
var BulletTTLValues = []float32{200, 2, 3, 4}
var BulletDamageValues = []float32{1, 2, 3, 4}
var HealthMaxValues = []float32{1, 2, 3, 4}
var HealthRegenerationValues = []float32{1, 2, 3, 4}
var BodyDamageValues = []float32{1, 2, 3, 4}
var ReloadSpeedValues = []int{1, 2, 3, 4}
var LevelUpdateExp = []int{5, 10, 20, 40}

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
	}{
		X:          p.X,
		Y:          p.Y,
		Angle:      p.Angle,
		Alive:      p.Alive,
		Id:         p.Id,
		Name:       p.Name,
		TankId:     p.Tank.TankId(),
		TankRadius: p.Tank.Radius(),
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

	if p.X != InRange(p.X, -p.World.Size, p.World.Size) ||
		p.Y != InRange(p.Y, -p.World.Size, p.World.Size) {
		p.Health -= PlayerOutOfWorldHealth
	}

	if p.Health < 0 {
		p.Alive = false
		if p.LifesLeft > 0 {
			p.RespawnPlayer()
		}
	}

	p.Health = float32(
		math.Min(
			float64(p.RealStatsValues().HealthMax),
			float64(p.Health+p.RealStatsValues().HealthRegeneration)),
	)

	for p.Exp > LevelUpdateExp[p.Level] {
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

func (p *Player) UpdateStat(stat Stat) {
	switch stat {
	case StatRange:
		if p.LevelsLeft > 0 && len(RangeValues) > p.Stats.Range {
			p.Stats.Range++
			p.LevelsLeft--
		}
		break
	case StatSpeed:
		if p.LevelsLeft > 0 && len(SpeedValues) > p.Stats.Speed {
			p.Stats.Speed++
			p.LevelsLeft--
		}
		break
	case StatBulletSpeed:
		if p.LevelsLeft > 0 && len(BulletSpeedValues) > p.Stats.BulletSpeed {
			p.Stats.BulletSpeed++
			p.LevelsLeft--
		}
		break
	case StatBulletTTL:
		if p.LevelsLeft > 0 && len(BulletTTLValues) > p.Stats.BulletTTL {
			p.Stats.BulletTTL++
			p.LevelsLeft--
		}
		break
	case StatBulletDamage:
		if p.LevelsLeft > 0 && len(BulletDamageValues) > p.Stats.BulletDamage {
			p.Stats.BulletDamage++
			p.LevelsLeft--
		}
		break
	case StatHealthMax:
		if p.LevelsLeft > 0 && len(HealthMaxValues) > p.Stats.HealthMax {
			p.Stats.HealthMax++
			p.LevelsLeft--
		}
		break
	case StatHealthRegeneration:
		if p.LevelsLeft > 0 && len(HealthRegenerationValues) > p.Stats.HealthRegeneration {
			p.Stats.HealthRegeneration++
			p.LevelsLeft--
		}
		break
	case StatBodyDamage:
		if p.LevelsLeft > 0 && len(BodyDamageValues) > p.Stats.BodyDamage {
			p.Stats.BodyDamage++
			p.LevelsLeft--
		}
		break
	case StatReloadSpeed:
		if p.LevelsLeft > 0 && len(ReloadSpeedValues) > p.Stats.ReloadSpeed {
			p.Stats.ReloadSpeed++
			p.LevelsLeft--
		}
		break
	}
}

func (p *Player) UpdateTank(newTank Tank) {
	if p.TankUpdatesLeft > 0 {
		p.Tank = newTank
		p.TankUpdatesLeft--
	}
}

func (p *Player) ReachablePlayers() []Player {
	var res []Player
	for _, player := range p.World.Players {
		if p.inReach(player.Position, p.RealStatsValues().Range) {
			res = append(res, player)
		}
	}
	return res
}

func (p *Player) ReachableEntities() []Entity {
	var res []Entity
	for _, entity := range p.World.Entities {
		if p.inReach(entity.Position, p.RealStatsValues().Range) {
			res = append(res, entity)
		}
	}
	return res
}

func (p *Player) ReachableBullets() []Bullet {
	var res []Bullet
	for _, bullet := range p.World.Bullets {
		if p.inReach(bullet.Position, p.RealStatsValues().Range) {
			res = append(res, bullet)
		}
	}
	return res
}

type PlayerMovement struct {
	OldPosition Position
	Player      *Player
}

func (pm *PlayerMovement) speed() float32 {
	return Distance(pm.OldPosition, pm.Player.Position)
}
