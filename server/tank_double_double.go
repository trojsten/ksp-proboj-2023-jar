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
	return StatsValues{
		Range:              0,
		Speed:              0,
		BulletSpeed:        0,
		BulletTTL:          0,
		BulletDamage:       0,
		HealthMax:          0,
		HealthRegeneration: 0,
		BodyDamage:         0,
		ReloadSpeed:        0,
	}
}

func (t DoubleDoubleTank) Radius() float32 {
	return 5
}

func (t DoubleDoubleTank) TankLevel() int {
	return 1
}

func (t DoubleDoubleTank) TankId() int {
	return 4
}

func (t DoubleDoubleTank) UpdatableTo() []Tank {
	return nil
}

func (t DoubleDoubleTank) KnockBack() float32 {
	return 5
}