package main

type Tank interface {
	Fire(player *Player, playerMovement PlayerMovement) (float32, float32)
	StatsValues() StatsValues
	Radius() float32
	TankLevel() int
	TankId() int
	UpdatableTo() []Tank
	KnockBack() float32
}

type BasicTank struct {
}

func (b BasicTank) Fire(player *Player, playerMovement PlayerMovement) (float32, float32) {
	var bullet = NewBullet(player.World, *player, playerMovement, player.Angle, 5) //TODO constant
	return bullet.Vx * b.KnockBack(), bullet.Vy * b.KnockBack()
}

func (b BasicTank) StatsValues() StatsValues {
	return StatsValues{}
}

func (b BasicTank) Radius() float32 {
	return 5
}

func (b BasicTank) TankLevel() int {
	return 0
}

func (b BasicTank) TankId() int {
	return 0
}

func (b BasicTank) UpdatableTo() []Tank {
	return nil
}

func (b BasicTank) KnockBack() float32 {
	return 5
}

func CanUpdateTank(t Tank, newTankId int) (bool, Tank) {
	for _, tank := range t.UpdatableTo() {
		if tank.TankId() == newTankId {
			return true, tank
		}
	}
	return false, nil
}
