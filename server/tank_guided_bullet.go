package main

type GuidedBulletTank struct {
	//TODO constants
}

func (t GuidedBulletTank) Fire(player *Player, playerMovement PlayerMovement, angle2 float32) (float32, float32) {
	// TODO guiding
	var bullet = NewBullet(player.World, player.Id, player.Position, player.RealStatsValues(), playerMovement, player.Angle, 5, true)
	return bullet.Vx * t.KnockBack(), bullet.Vy * t.KnockBack()
}

func (t GuidedBulletTank) StatsValues() StatsValues {
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

func (t GuidedBulletTank) Radius() float32 {
	return 5
}

func (t GuidedBulletTank) TankLevel() int {
	return 0
}

func (t GuidedBulletTank) TankId() int {
	return 7
}

func (t GuidedBulletTank) UpdatableTo() []Tank {
	return nil
}

func (t GuidedBulletTank) KnockBack() float32 {
	return 5
}
