package main

import "math"

type Bullet struct {
	Position
	Vx        float32
	Vy        float32
	TTL       int
	Damage    int
	ShooterId int
}

// Tick moves the given bullet and returns whether it's entity should be removed
func (b *Bullet) Tick(w *World) bool {
	if b.TTL <= 0 {
		return false
	}

	// TODO: Check in-flight collisions

	b.X += b.Vx
	b.Y += b.Vy
	b.TTL--
	return true
}

func NewBullet(w *World, player Player, angle float32) *Bullet {
	var bulletSpeed float32 = 1 // TODO real bullet speed
	bullet := Bullet{
		Position:  player.Position,
		Vx:        float32(math.Cos(float64(angle))) * bulletSpeed,
		Vy:        float32(math.Sin(float64(angle))) * bulletSpeed,
		TTL:       0, // TODO real TTL
		Damage:    0, // TODO real damage
		ShooterId: player.Id,
	}
	w.Bullets = append(w.Bullets, bullet)
	return &bullet
}
