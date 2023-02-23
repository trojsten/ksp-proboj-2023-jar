package main

type Tank interface {
	Fire(w *World, player Player)
	StatsValues() StatsValues
	Radius() float32
	TankLevel() int
}

type BasicTank struct {
}

func (b BasicTank) Fire(w *World, player Player) {
	NewBullet(w, player, player.Angle)
}

func (b BasicTank) StatsValues() StatsValues {
	return StatsValues{}
}

func (b BasicTank) Radius() float32 {
	return 5
}

func (b BasicTank) TankLevel() int {
	return 0
}
