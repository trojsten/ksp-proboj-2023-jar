package main

import "fmt"

type Stat int

const (
	StatNone Stat = iota
	StatRange
	StatSpeed
	StatBulletSpeed
	StatBulletTTL
	StatBulletDamage
	StatHelathMax
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

type Player struct {
	Position
	Id             int
	Name           string
	Alive          bool
	Health         int
	Exp            int
	Level          int
	Angle          float32
	Stats          Stats
	Tank           Tank
	World          *World
	ReloadCooldown int
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
func (p *Player) MoveTo(x, y float32) {
	p.X = InRange(x, -p.World.Size, p.World.Size)
	p.Y = InRange(y, -p.World.Size, p.World.Size)
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

	p.MoveTo(p.X, p.Y) // This will move the player back to the world if positioned outside of it's border
}
