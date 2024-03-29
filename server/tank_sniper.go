package main

type SniperTank struct {
	//TODO constants
}

func (t SniperTank) Fire(player *Player, playerMovement PlayerMovement, angle2 float32, target Target) (float32, float32) {
	var bullet = NewBullet(player.World, player.Id, player.Position, player.RealStatsValues(), playerMovement, player.Angle, 5, true, nil)
	return bullet.Vx * t.KnockBack(), bullet.Vy * t.KnockBack()
}

func (t SniperTank) StatsValues() StatsValues {
	return StatsValues{
		Range:              400,
		Speed:              0,
		BulletSpeed:        10,
		BulletTTL:          0,
		BulletDamage:       0,
		HealthMax:          0,
		HealthRegeneration: 0,
		BodyDamage:         0,
		ReloadSpeed:        6,
	}
}

func (t SniperTank) CoefStatsValues() StatsValues {
	return StatsValues{
		Range:              1,
		Speed:              1,
		BulletSpeed:        1,
		BulletTTL:          1.5,
		BulletDamage:       2,
		HealthMax:          1,
		HealthRegeneration: 1,
		BodyDamage:         1,
		ReloadSpeed:        1,
	}
}

func (t SniperTank) Radius() float32 {
	return 5
}

func (t SniperTank) TankLevel() int {
	return 0
}

func (t SniperTank) TankId() int {
	return 5
}

func (t SniperTank) UpdatableTo() []Tank {
	return []Tank{WideBulletTank{}, GuidedBulletTank{}, MachineGunTank{}}
}

func (t SniperTank) KnockBack() float32 {
	return -0.2
}
