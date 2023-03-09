package main

type TwinTank struct {
	//TODO constants
}

func (t TwinTank) Fire(player *Player, playerMovement PlayerMovement) (float32, float32) {
	return TwinShot(player, playerMovement, t.KnockBack(), player.Angle)
}

func (t TwinTank) StatsValues() StatsValues {
	return StatsValues{}
}

func (t TwinTank) Radius() float32 {
	return 5
}

func (t TwinTank) TankLevel() int {
	return 1
}

func (t TwinTank) TankId() int {
	return 1
}

func (t TwinTank) UpdatableTo() []Tank {
	return []Tank{EverywhereTank{}, DoubleDoubleTank{}}
}

func (t TwinTank) KnockBack() float32 {
	return 5
}
