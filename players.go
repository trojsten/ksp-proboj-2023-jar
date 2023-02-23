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
	Id     int
	Name   string
	X      float32
	Y      float32
	Health int
	Stats  Stats
}

func NewPlayer(name string) Player {
	return Player{Name: name}
}
