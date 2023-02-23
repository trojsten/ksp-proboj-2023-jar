package main

import (
	"fmt"
	"github.com/trojsten/ksp-proboj/libproboj"
)

// Tick executes one game tick
func (w *World) Tick() {
	for _, player := range w.Players {
		w.Runner.ToPlayer(player.Name, fmt.Sprintf("TICK %d", w.TickNumber), w.DataForPlayer(player))
		resp, data := w.Runner.ReadPlayer(player.Name)
		if resp != libproboj.Ok {
			w.Runner.Log(fmt.Sprintf("bad response while reading player %s: %s", player.Name, resp))
		}
		w.Runner.Log(data)
		// TODO: Handle player response
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
}
