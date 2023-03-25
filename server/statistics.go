package main

type Statistics struct {
	TimeByTank        map[int]int
	ScoreByReason     map[Reason]int
	TimeInCooldown    int
	TimeNotInCooldown int
	TimeOfResponses   int64
}

type Reason int

const (
	BodyDamagePlayer Reason = iota
	BulletDamagePlayer
	BodyDamageEntity
	BulletDamageEntity
	KillPlayer
	KillEntity
)
