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
	for _, player := range players {
		world.Players = append(world.Players, NewPlayer(player))
	}

	for world.Running() {
		world.Tick()
	}
}
