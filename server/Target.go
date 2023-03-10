package main

import "math"

type Target interface {
	Angle(position Position) float32
}

type PositionTarget struct {
	TargetPosition Position
}

func (p PositionTarget) Angle(position Position) float32 {
	return float32(math.Atan2(float64(p.TargetPosition.Y-position.Y), float64(p.TargetPosition.X-position.X)))
}

type PlayerTarget struct {
	Player Player
}

func (p PlayerTarget) Angle(position Position) float32 {
	return float32(math.Atan2(float64(p.Player.Y-position.Y), float64(p.Player.X-position.X)))
}
