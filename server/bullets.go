package main

import "math"

type Bullet struct {
	Position  `json:"position"`
	Id        int     `json:"id"`
	Radius    float32 `json:"radius"`
	Vx        float32 `json:"-"`
	Vy        float32 `json:"-"`
	TTL       float32 `json:"-"`
	Damage    float32 `json:"-"`
	ShooterId int     `json:"shooter_id"`
	Visible   bool    `json:"visible"`
}

// Tick moves the given bullet and returns whether it's entity should be removed
func (b *Bullet) Tick() (bool, BulletMovement) {
	if b.TTL <= 0 {
		return false, BulletMovement{}
	}

	var bulletMovement = BulletMovement{OldPosition: b.Position, Bullet: b}

	b.X += b.Vx
	b.Y += b.Vy
	b.TTL--
	return true, bulletMovement
}

func NewBullet(w *World, playerId int, position Position, statsValues StatsValues, playerMovement PlayerMovement, angle float32, radius float32, visible bool) *Bullet {
	var bulletSpeed = statsValues.BulletSpeed

	var Vx = float32(math.Cos(float64(angle))) * bulletSpeed
	var Vy = float32(math.Sin(float64(angle))) * bulletSpeed
	var Px = playerMovement.NewPosition.X - playerMovement.Player.Position.X
	var Py = playerMovement.NewPosition.Y - playerMovement.Player.Position.Y

	bullet := Bullet{
		Position:  position,
		Id:        w.BulletNumber,
		Radius:    radius,
		Vx:        Vx + FractionOfPlayerSpeedToBullet*Px,
		Vy:        Vy + FractionOfPlayerSpeedToBullet*Py,
		TTL:       statsValues.BulletTTL,
		Damage:    statsValues.BulletDamage,
		ShooterId: playerId,
		Visible:   visible,
	}
	w.BulletNumber++
	w.Bullets = append(w.Bullets, bullet)
	return &bullet
}

type BulletMovement struct {
	OldPosition Position
	Bullet      *Bullet
}
