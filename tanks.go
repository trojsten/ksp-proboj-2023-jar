package main

type Tank interface {
	Fire(w *World, player Player)
	Stats() Stats
	Radius() float32
	TankLevel() int
}

type BasicTank struct {
}

func (b BasicTank) Fire(w *World, player Player) {
	NewBullet(w, player, player.Angle)
}

func (b BasicTank) Stats() Stats {
	return Stats{}
}

func (b BasicTank) Radius() float32 {
	return 5
}

func (b BasicTank) TankLevel() int {
	return 0
}
