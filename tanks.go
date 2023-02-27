package main

type Tank interface {
	Fire(player *Player)
	StatsValues() StatsValues
	Radius() float32
	TankLevel() int
	TankId() int
}

type BasicTank struct {
}

func (b BasicTank) Fire(player *Player) {
	NewBullet(player.World, *player, player.Angle)
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

func (b BasicTank) TankId() int {
	return 0
}
