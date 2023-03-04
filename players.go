package main

import (
	"fmt"
	"math"
)

type Stat int

const (
	StatNone Stat = iota
	StatRange
	StatSpeed
	StatBulletSpeed
	StatBulletTTL
	StatBulletDamage
	StatHealthMax
	StatHealthRegeneration
	StatBodyDamage
	StatReloadSpeed
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
var BulletTTLValues = []float32{1, 2, 3, 4}
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
}

func (w *World) NewPlayer(name string) Player {
	return Player{Name: name, Tank: BasicTank{}, Alive: true, World: w}
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
	p.X = InRange(x, -p.World.Size, p.World.Size)
	p.Y = InRange(y, -p.World.Size, p.World.Size)
	return movement
}

func (p *Player) Fire() {
	if p.ReloadCooldown > 0 {
		p.World.Runner.Log(fmt.Sprintf("ignoring shoot for %s: reload cooldown", p.Name))
		return
	}

	p.Tank.Fire(p)
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
		// TODO ozivovanie?
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

type PlayerMovement struct {
	OldPosition Position
	Player      *Player
}
