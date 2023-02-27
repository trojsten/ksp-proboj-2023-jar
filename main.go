package main

import (
	"fmt"
	"github.com/trojsten/ksp-proboj/libproboj"
	"math/rand"
	"time"
)

func main() {
	runner := libproboj.NewRunner()
	seed := time.Now().UnixMilli()
	rand.Seed(seed)
	runner.Log(fmt.Sprintf("seed %d", seed))

	world := World{Runner: runner}
	players, _ := runner.ReadConfig()
	for i, player := range players {
		pl := world.NewPlayer(player)
		pl.Id = i
		world.Players = append(world.Players, pl)
	}

	for world.Running() {
		world.Tick()
	}
}
