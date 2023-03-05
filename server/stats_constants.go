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

var RangeValues = []float32{300, 400, 500, 600, 700, 800, 900, 1000}
var SpeedValues = []float32{30, 33, 36, 40, 43, 46, 50, 55}
var BulletSpeedValues = []float32{70, 75, 80, 85, 90, 95, 100, 105}
var BulletTTLValues = []float32{10, 10, 10, 10, 10, 10, 10, 10}
var BulletDamageValues = []float32{30, 40, 50, 60, 70, 80, 90, 100}
var HealthMaxValues = []float32{500, 550, 600, 650, 700, 750, 800, 850}
var HealthRegenerationValues = []float32{0, 5, 10, 15, 20, 25, 30, 35}
var BodyDamageValues = []float32{0, 10, 20, 30, 40, 50, 60, 70}
var ReloadSpeedValues = []int{10, 9, 8, 7, 6, 5, 4, 3, 2, 1}
var LevelUpdateExp = []int{1, 2, 3, 4}