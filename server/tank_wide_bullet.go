package main

type WideBulletTank struct {
	//TODO constants
}

func (t WideBulletTank) Fire(player *Player, playerMovement PlayerMovement) (float32, float32) {
	var bullet = NewBullet(player.World, player.Id, player.Position, player.RealStatsValues(), playerMovement, player.Angle, 15)
	return bullet.Vx * t.KnockBack(), bullet.Vy * t.KnockBack()
}

func (t WideBulletTank) StatsValues() StatsValues {
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

func (t WideBulletTank) Radius() float32 {
	return 5
}

func (t WideBulletTank) TankLevel() int {
	return 0
}

func (t WideBulletTank) TankId() int {
	return 6
}

func (t WideBulletTank) UpdatableTo() []Tank {
	return nil
}

func (t WideBulletTank) KnockBack() float32 {
	return 5
}
