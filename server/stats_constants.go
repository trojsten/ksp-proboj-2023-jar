package main

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
