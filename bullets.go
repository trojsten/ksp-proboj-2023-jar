package main

type Bullet struct {
	X         float32
	Y         float32
	Vx        float32
	Vy        float32
	TTL       int
	Damage    int
	ShooterId int
}

// Tick moves the given bullet and returns whether it's entity should be removed
func (b *Bullet) Tick() bool {
	if b.TTL <= 0 {
		return false
	}

	// TODO: Check in-flight collisions

	b.X += b.Vx
	b.Y += b.Vy
	b.TTL--
	return true
}
