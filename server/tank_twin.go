package main

type TwinTank struct {
	//TODO constants
}

func (t TwinTank) Fire(player *Player, playerMovement PlayerMovement) (float32, float32) {
	return TwinShot(player, playerMovement, t.KnockBack(), player.Angle)
}

func (t TwinTank) StatsValues() StatsValues {
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
	return []Tank{EverywhereTank{}, DoubleDoubleTank{}, VariableDoubleTank{}}
}

func (t TwinTank) KnockBack() float32 {
	return 5
}