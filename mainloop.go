package main

import (
	"fmt"
	"github.com/trojsten/ksp-proboj/libproboj"
)

// Tick executes one game tick
func (w *World) Tick() {
	for i, player := range w.Players {
		w.Runner.ToPlayer(player.Name, fmt.Sprintf("TICK %d", w.TickNumber), w.DataForPlayer(player))
		resp, data := w.Runner.ReadPlayer(player.Name)
		if resp != libproboj.Ok {
			w.Runner.Log(fmt.Sprintf("bad response while reading player %s: %s", player.Name, resp))
			continue
		}
		w.Runner.Log(data)
		err := w.ParseResponse(data, &w.Players[i])
		if err != nil {
			w.Runner.Log(fmt.Sprintf("error while parsing response from %s: %s", player.Name, err.Error()))
			continue
		}
	}

	// Bullet time!
	var bullets []Bullet
	for i := range w.Bullets {
		bullet := &w.Bullets[i]
		if bullet.Tick(w) {
			bullets = append(bullets, *bullet)
		}
	}
	w.Bullets = bullets

	// Update players
	for i := range w.Players {
		w.Players[i].Tick()
	}
}
