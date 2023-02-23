package main

type Tank interface {
	Fire(w *World, player Player)
	Stats() Stats
	Radius() float32
}

type BasicTank struct {
}

func (b BasicTank) Fire(w *World, player Player) {
	NewBullet(w, player, 0) // TODO angle
}

func (b BasicTank) Stats() Stats {
	return Stats{}
}

func (b BasicTank) Radius() float32 {
	return 5
}
