package main

type VariableDoubleTank struct {
	//TODO constants
}

func (t VariableDoubleTank) Fire(player *Player, playerMovement PlayerMovement) (float32, float32) {
	// TODO two angles
	var bullet1 = NewBullet(player.World, player.Id, player.Position, player.RealStatsValues(), playerMovement, player.Angle, 5, true)
	var bullet2 = NewBullet(player.World, player.Id, player.Position, player.RealStatsValues(), playerMovement, player.Angle, 5, true)
	return (bullet1.Vx + bullet2.Vx) * t.KnockBack(), (bullet1.Vy + bullet2.Vy) * t.KnockBack()
}

func (t VariableDoubleTank) StatsValues() StatsValues {
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

func (t VariableDoubleTank) Radius() float32 {
	return 5
}

func (t VariableDoubleTank) TankLevel() int {
	return 1
}

func (t VariableDoubleTank) TankId() int {
	return 3
}

func (t VariableDoubleTank) UpdatableTo() []Tank {
	return nil
}

func (t VariableDoubleTank) KnockBack() float32 {
	return 5
}
