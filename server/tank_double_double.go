package main

import "math"

type DoubleDoubleTank struct {
	//TODO constants
}

func (t DoubleDoubleTank) Fire(player *Player, playerMovement PlayerMovement) (float32, float32) {
	TwinShot(player, playerMovement, t.KnockBack(), player.Angle)
	TwinShot(player, playerMovement, t.KnockBack(), player.Angle+math.Pi)
	return 0, 0
}

func (t DoubleDoubleTank) StatsValues() StatsValues {
	return StatsValues{}
}

func (t DoubleDoubleTank) Radius() float32 {
	return 5
}

func (t DoubleDoubleTank) TankLevel() int {
	return 1
}

func (t DoubleDoubleTank) TankId() int {
	return 3
}

func (t DoubleDoubleTank) UpdatableTo() []Tank {
	return nil
}

func (t DoubleDoubleTank) KnockBack() float32 {
	return 5
}
