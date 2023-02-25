package main

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
	ReloadSpeed        float32
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
var ReloadSpeedValues = []float32{1, 2, 3, 4}

type Player struct {
	Position
	Id     int
	Name   string
	Alive  bool
	Health int
	Exp    int
	Level  int
	Angle  float32
	Stats  Stats
	Tank   Tank
}

func NewPlayer(name string) Player {
	return Player{Name: name, Tank: BasicTank{}, Alive: true}
}

func (player Player) RealStatsValues() StatsValues {
	var tankStats = player.Tank.StatsValues()

	return StatsValues{
		RangeValues[player.Stats.Range] + tankStats.Range,
		SpeedValues[player.Stats.Speed] + tankStats.Speed,
		BulletSpeedValues[player.Stats.BulletSpeed] + tankStats.BulletSpeed,
		BulletTTLValues[player.Stats.BulletTTL] + tankStats.BulletTTL,
		BulletDamageValues[player.Stats.BulletDamage] + tankStats.BulletDamage,
		HealthMaxValues[player.Stats.HealthMax] + tankStats.HealthMax,
		HealthRegenerationValues[player.Stats.HealthRegeneration] + tankStats.HealthRegeneration,
		BodyDamageValues[player.Stats.BodyDamage] + tankStats.BodyDamage,
		ReloadSpeedValues[player.Stats.ReloadSpeed] + tankStats.ReloadSpeed,
	}
}
