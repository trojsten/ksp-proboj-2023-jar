package main

type BasicTank struct {
	//TODO constants
}

func (t BasicTank) Fire(player *Player, playerMovement PlayerMovement) (float32, float32) {
	var bullet = NewBullet(player.World, player.Id, player.Position, player.RealStatsValues(), playerMovement, player.Angle, 5)
	return bullet.Vx * t.KnockBack(), bullet.Vy * t.KnockBack()
}

func (t BasicTank) StatsValues() StatsValues {
	return StatsValues{}
}

func (t BasicTank) Radius() float32 {
	return 5
}

func (t BasicTank) TankLevel() int {
	return 0
}

func (t BasicTank) TankId() int {
	return 0
}

func (t BasicTank) UpdatableTo() []Tank {
	return []Tank{TwinTank{}}
}

func (t BasicTank) KnockBack() float32 {
	return 5
}
