package main

import "math"

type Bullet struct {
	Position
	Radius    float32
	Vx        float32
	Vy        float32
	TTL       float32
	Damage    float32
	ShooterId int
}

// Tick moves the given bullet and returns whether it's entity should be removed
func (b *Bullet) Tick(w *World) (bool, BulletMovement) {
	if b.TTL <= 0 {
		return false, BulletMovement{}
	}

	// TODO: Check in-flight collisions

	var bulletMovement = BulletMovement{OldPosition: b.Position}

	b.X += b.Vx
	b.Y += b.Vy
	b.TTL--
	return true, bulletMovement
}

func NewBullet(w *World, player Player, angle float32, radius float32) *Bullet {
	var statsValues = player.RealStatsValues()
	var bulletSpeed = statsValues.BulletSpeed
	bullet := Bullet{
		Position:  player.Position,
		Vx:        float32(math.Cos(float64(angle))) * bulletSpeed,
		Vy:        float32(math.Sin(float64(angle))) * bulletSpeed,
		TTL:       statsValues.BulletTTL,
		Damage:    statsValues.BulletDamage,
		ShooterId: player.Id,
	}
	w.Bullets = append(w.Bullets, bullet)
	return &bullet
}

type BulletMovement struct {
	OldPosition Position
	Bullet      *Bullet
}
