package main

type Stats struct {
	Range              int
	Speed              int
	BulletSpeed        int
	BulletTTL          int
	BulletDamage       int
	HealthMax          int
	HealthRegeneration int
	BodyDamage         int
	ReloadSpeed        int
}

type Player struct {
	Position
	Id     int
	Name   string
	Alive  bool
	Health int
	Exp    int
	Level  int
	Stats  Stats
	Tank   Tank
}

func NewPlayer(name string) Player {
	return Player{Name: name}
}

func (player Player) getRange() float32 {
	// TODO
	return 0
}
