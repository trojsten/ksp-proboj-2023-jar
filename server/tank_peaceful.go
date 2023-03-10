package main

type PeacefulTank struct {
	//TODO constants
}

func (t PeacefulTank) Fire(player *Player, playerMovement PlayerMovement) (float32, float32) {
	return 0, 0
}

func (t PeacefulTank) StatsValues() StatsValues {
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

func (t PeacefulTank) Radius() float32 {
	return 5
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
	return 5
}