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

	world := World{Runner: runner, MinX: MinX, MaxX: MaxX, MinY: MinY, MaxY: MaxY, Bullets: []Bullet{}}
	players, _ := runner.ReadConfig()
	for i, player := range players {
		pl := world.NewPlayer(player)
		pl.Id = i
		world.SpawnObject(&pl.Position)
		world.Players = append(world.Players, pl)
	}

	for i := 0; i < EntitiesInitSpawnNumber; i++ {
		world.SpawnEntity()
	}

	for world.Running() {
		world.Tick()
		// TODO constants and min world size
		if world.TickNumber > ShrinkWorldAfter {
			world.MinX *= WorldSizeShrink
			world.MaxX *= WorldSizeShrink
			world.MinY *= WorldSizeShrink
			world.MaxY *= WorldSizeShrink
		}

		if rand.Float32() < EntitySpawnProb {
			world.SpawnEntity()
		}
		world.TickNumber++
	}
}
