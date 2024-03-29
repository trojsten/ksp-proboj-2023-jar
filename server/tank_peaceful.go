package main

type PeacefulTank struct {
	//TODO constants
}

func (t PeacefulTank) Fire(player *Player, playerMovement PlayerMovement, angle2 float32, target Target) (float32, float32) {
	return 0, 0
}

func (t PeacefulTank) StatsValues() StatsValues {
	return StatsValues{
		Range:              150,
		Speed:              5,
		BulletSpeed:        0,
		BulletTTL:          0,
		BulletDamage:       0,
		HealthMax:          100,
		HealthRegeneration: 0,
		BodyDamage:         3,
		ReloadSpeed:        0,
	}
}

func (t PeacefulTank) CoefStatsValues() StatsValues {
	return StatsValues{
		Range:              1,
		Speed:              1.1,
		BulletSpeed:        1,
		BulletTTL:          1,
		BulletDamage:       1,
		HealthMax:          1.5,
		HealthRegeneration: 1,
		BodyDamage:         3,
		ReloadSpeed:        1,
	}
}

func (t PeacefulTank) Radius() float32 {
	return 15
}

func (t PeacefulTank) TankLevel() int {
	return 0
}

func (t PeacefulTank) TankId() int {
	return 10
}

func (t PeacefulTank) UpdatableTo() []Tank {
	return nil
}

func (t PeacefulTank) KnockBack() float32 {
	return 0
}
